from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from django.db.models import Prefetch, Q
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .models import Task, TaskHistory
from .serializers import TaskSerializer, TaskHistorySerializer


class TaskViewSet(viewsets.ModelViewSet):
    """Enhanced TaskViewSet with caching and query optimization.
    
    Features:
    - Redis caching for list endpoint (5 minutes)
    - Query optimization with select_related/prefetch_related
    - Soft delete instead of hard delete
    - Advanced filtering (status, priority, tags)
    - Task history tracking
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Optimized queryset with filters and soft delete awareness."""
        # Base queryset with optimizations
        queryset = Task.objects.filter(
            user=self.request.user,
            is_deleted=False
        ).select_related('user').prefetch_related(
            Prefetch(
                'history',
                queryset=TaskHistory.objects.select_related('changed_by').order_by('-changed_at')[:5]
            )
        )
        
        # Apply filters from query params
        status_filter = self.request.query_params.get('status')
        priority_filter = self.request.query_params.get('priority')
        tags_filter = self.request.query_params.get('tags')
        overdue = self.request.query_params.get('overdue')
        
        if status_filter:
            queryset = queryset.filter(status=status_filter.upper())
        
        if priority_filter:
            queryset = queryset.filter(priority=priority_filter.upper())
        
        if tags_filter:
            # Search for tasks with any of the specified tags
            tag_queries = Q()
            for tag in tags_filter.split(','):
                tag_queries |= Q(tags__icontains=tag.strip())
            queryset = queryset.filter(tag_queries)
        
        if overdue == 'true':
            queryset = queryset.filter(
                due_date__lt=timezone.now().date(),
                status__in=[Task.Status.TODO, Task.Status.DOING]
            )
        
        # Default ordering: priority (HIGH first), then due_date, then created
        return queryset.order_by(
            '-priority',  # HIGH > MEDIUM > LOW (reverse alphabetical)
            'due_date',   # Nearest deadline first
            '-created_at' # Most recent first
        )
    
    def list(self, request, *args, **kwargs):
        """List tasks with caching."""
        # Generate cache key based on user and filters
        query_params = request.query_params.urlencode()
        cache_key = f'tasks_list_{request.user.id}_{query_params}'
        
        # Try to get from cache
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        
        # If not in cache, fetch from database
        response = super().list(request, *args, **kwargs)
        
        # Cache the response for 5 minutes
        cache.set(cache_key, response.data, 60 * 5)
        
        return response
    
    def perform_create(self, serializer):
        """Create task with current user."""
        task = serializer.save(user=self.request.user)
        
        # Clear user's task list cache
        self._clear_user_cache()
        
        # Log creation in history
        TaskHistory.objects.create(
            task=task,
            changed_by=self.request.user,
            field_name='created',
            old_value='',
            new_value='Task created'
        )
    
    def perform_update(self, serializer):
        """Update task and track changes in history."""
        old_instance = self.get_object()
        
        # Track changes
        changes = []
        for field in ['title', 'description', 'status', 'priority', 'due_date', 'tags']:
            old_value = getattr(old_instance, field)
            new_value = serializer.validated_data.get(field, old_value)
            
            if old_value != new_value:
                changes.append({
                    'field_name': field,
                    'old_value': str(old_value) if old_value else '',
                    'new_value': str(new_value) if new_value else ''
                })
        
        # Save the task
        task = serializer.save()
        
        # Mark as completed if status changed to DONE
        if task.status == Task.Status.DONE and not task.completed_at:
            task.mark_completed()
        
        # Log changes to history
        for change in changes:
            TaskHistory.objects.create(
                task=task,
                changed_by=self.request.user,
                **change
            )
        
        # Clear cache
        self._clear_user_cache()
    
    def perform_destroy(self, instance):
        """Soft delete instead of hard delete."""
        instance.soft_delete()
        
        # Log deletion
        TaskHistory.objects.create(
            task=instance,
            changed_by=self.request.user,
            field_name='deleted',
            old_value='active',
            new_value='deleted'
        )
        
        # Clear cache
        self._clear_user_cache()
    
    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        """Restore a soft-deleted task."""
        task = self.get_object()
        
        if not task.is_deleted:
            return Response(
                {'detail': 'Task is not deleted'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        task.restore()
        
        # Log restoration
        TaskHistory.objects.create(
            task=task,
            changed_by=request.user,
            field_name='restored',
            old_value='deleted',
            new_value='active'
        )
        
        # Clear cache
        self._clear_user_cache()
        
        return Response(
            TaskSerializer(task).data,
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        """Get task change history."""
        task = self.get_object()
        history = task.history.all()[:20]  # Last 20 changes
        serializer = TaskHistorySerializer(history, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get task statistics for current user."""
        tasks = Task.objects.filter(user=request.user, is_deleted=False)
        
        stats = {
            'total': tasks.count(),
            'by_status': {
                'todo': tasks.filter(status=Task.Status.TODO).count(),
                'doing': tasks.filter(status=Task.Status.DOING).count(),
                'done': tasks.filter(status=Task.Status.DONE).count(),
            },
            'by_priority': {
                'low': tasks.filter(priority=Task.Priority.LOW).count(),
                'medium': tasks.filter(priority=Task.Priority.MEDIUM).count(),
                'high': tasks.filter(priority=Task.Priority.HIGH).count(),
            },
            'overdue': tasks.filter(
                due_date__lt=timezone.now().date(),
                status__in=[Task.Status.TODO, Task.Status.DOING]
            ).count(),
            'completed_today': tasks.filter(
                completed_at__date=timezone.now().date()
            ).count(),
        }
        
        return Response(stats)
    
    def _clear_user_cache(self):
        """Clear all task list cache for current user."""
        # Clear cache with pattern matching
        cache_pattern = f'tasks_list_{self.request.user.id}_*'
        cache.delete_pattern(cache_pattern)

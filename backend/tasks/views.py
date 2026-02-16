from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache
from django.utils import timezone
from .models import Task, TaskHistory
from .serializers import TaskSerializer, TaskHistorySerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority']
    search_fields = ['title', 'description', 'tags']
    # Add default ordering to prevent slicing errors
    ordering_fields = ['due_date', 'priority', 'created_date']
    ordering = ['-created_date']

    def get_queryset(self):
        # Use all_objects to access deleted tasks if needed
        manager = Task.all_objects if hasattr(Task, 'all_objects') else Task.objects
        queryset = manager.filter(user=self.request.user)

        # If action is restore or history, show deleted tasks too
        if self.action in ['restore', 'history', 'retrieve']:
            return queryset
        
        # Otherwise (normal list), show only live tasks
        return queryset.filter(is_deleted=False)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        self._clear_user_cache()

    def perform_update(self, serializer):
        serializer.save()
        self._clear_user_cache()

    def perform_destroy(self, instance):
        instance.soft_delete()
        self._clear_user_cache()

    def _clear_user_cache(self):
        # Handle LocMemCache bug in tests
        cache_pattern = f'tasks_list_{self.request.user.id}_*'
        if hasattr(cache, 'delete_pattern'):
            cache.delete_pattern(cache_pattern)
        else:
            # In test environment where Redis is not present, clear all cache (safe for tests)
            cache.clear()

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        try:
            # Try to find task (even if deleted)
            task = self.get_queryset().get(pk=pk)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        task.restore()
        self._clear_user_cache()
        return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        try:
            task = self.get_queryset().get(pk=pk)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        history = TaskHistory.objects.filter(task=task).order_by('-changed_at')
        serializer = TaskHistorySerializer(history, many=True)
        return Response(serializer.data)

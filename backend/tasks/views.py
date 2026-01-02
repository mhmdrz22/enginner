from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """ViewSet for Task CRUD operations.
    
    Automatically filtered to show only tasks belonging to the authenticated user.
    Supports filtering by status and search by title/description.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'priority']
    ordering = ['-created_at']
    
    # Disable pagination to return simple list instead of paginated response
    pagination_class = None

    def get_queryset(self):
        """Return only tasks belonging to the current user."""
        return Task.objects.filter(user=self.request.user).select_related('user')

    def perform_create(self, serializer):
        """Automatically set the user when creating a task."""
        serializer.save(user=self.request.user)

from rest_framework import serializers
from .models import Task, TaskHistory


class TaskSerializer(serializers.ModelSerializer):
    """Enhanced Task serializer with computed fields."""
    
    is_overdue = serializers.ReadOnlyField()
    status_display = serializers.ReadOnlyField()
    priority_display = serializers.ReadOnlyField()
    tags_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Task
        fields = [
            'id', 'user', 'title', 'description',
            'status', 'status_display',
            'priority', 'priority_display',
            'due_date', 'tags', 'tags_list',
            'created_at', 'updated_at', 'completed_at',
            'is_overdue', 'is_deleted', 'deleted_at'
        ]
        read_only_fields = [
            'id', 'user', 'created_at', 'updated_at',
            'completed_at', 'is_deleted', 'deleted_at',
            'is_overdue', 'status_display', 'priority_display'
        ]
    
    def get_tags_list(self, obj):
        """Return tags as a list."""
        return obj.get_tags_list()
    
    def validate_due_date(self, value):
        """Ensure due date is not in the past for new tasks."""
        if value and not self.instance:
            from django.utils import timezone
            if value < timezone.now().date():
                raise serializers.ValidationError(
                    "Due date cannot be in the past for new tasks."
                )
        return value
    
    def validate_tags(self, value):
        """Validate tags format."""
        if value:
            tags = [tag.strip() for tag in value.split(',')]
            if len(tags) > 10:
                raise serializers.ValidationError(
                    "Maximum 10 tags allowed."
                )
            for tag in tags:
                if len(tag) > 50:
                    raise serializers.ValidationError(
                        "Each tag must be 50 characters or less."
                    )
        return value


class TaskHistorySerializer(serializers.ModelSerializer):
    """Serializer for task history entries."""
    
    changed_by_email = serializers.EmailField(source='changed_by.email', read_only=True)
    changed_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = TaskHistory
        fields = [
            'id', 'task', 'changed_by', 'changed_by_email', 'changed_by_name',
            'field_name', 'old_value', 'new_value', 'changed_at'
        ]
        read_only_fields = '__all__'
    
    def get_changed_by_name(self, obj):
        """Get user's full name or email."""
        if obj.changed_by:
            return obj.changed_by.get_full_name()
        return 'System'


class TaskCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for task creation."""
    
    tags_list = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False,
        write_only=True
    )
    
    class Meta:
        model = Task
        fields = [
            'title', 'description', 'status', 'priority',
            'due_date', 'tags', 'tags_list'
        ]
    
    def create(self, validated_data):
        tags_list = validated_data.pop('tags_list', None)
        
        if tags_list:
            validated_data['tags'] = ','.join(tags_list)
        
        return super().create(validated_data)

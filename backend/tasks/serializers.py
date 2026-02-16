from rest_framework import serializers
from .models import Task, TaskHistory

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'user', 'deleted_at', 'is_deleted')

class TaskHistorySerializer(serializers.ModelSerializer):
    changed_by = serializers.StringRelatedField()
    
    class Meta:
        model = TaskHistory
        fields = '__all__'
        read_only_fields = ('changed_at',)

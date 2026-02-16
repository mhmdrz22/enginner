import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { taskService } from '@/services/taskService'
import { toast } from 'sonner'
import type { Task, TaskFilters } from '@/types'

export function useTasks(filters?: TaskFilters) {
  const queryClient = useQueryClient()

  const { data: tasks, isLoading, error } = useQuery({
    queryKey: ['tasks', filters],
    queryFn: () => taskService.getTasks(filters),
  })

  const createMutation = useMutation({
    mutationFn: taskService.createTask,
    onSuccess: () => {
      queryClient.invalidateQueries(['tasks'])
      toast.success('Task created successfully')
    },
    onError: () => {
      toast.error('Failed to create task')
    },
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<Task> }) =>
      taskService.updateTask(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries(['tasks'])
      toast.success('Task updated successfully')
    },
    onError: () => {
      toast.error('Failed to update task')
    },
  })

  const deleteMutation = useMutation({
    mutationFn: taskService.deleteTask,
    onSuccess: () => {
      queryClient.invalidateQueries(['tasks'])
      toast.success('Task deleted successfully')
    },
    onError: () => {
      toast.error('Failed to delete task')
    },
  })

  return {
    tasks: tasks || [],
    isLoading,
    error,
    createTask: createMutation.mutate,
    updateTask: updateMutation.mutate,
    deleteTask: deleteMutation.mutate,
    isCreating: createMutation.isLoading,
    isUpdating: updateMutation.isLoading,
    isDeleting: deleteMutation.isLoading,
  }
}

export function useTask(id: number) {
  const queryClient = useQueryClient()

  const { data: task, isLoading, error } = useQuery({
    queryKey: ['task', id],
    queryFn: () => taskService.getTask(id),
    enabled: !!id,
  })

  const { data: history } = useQuery({
    queryKey: ['task-history', id],
    queryFn: () => taskService.getTaskHistory(id),
    enabled: !!id,
  })

  const updateMutation = useMutation({
    mutationFn: (data: Partial<Task>) => taskService.updateTask(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries(['task', id])
      queryClient.invalidateQueries(['tasks'])
      toast.success('Task updated successfully')
    },
    onError: () => {
      toast.error('Failed to update task')
    },
  })

  return {
    task,
    history: history || [],
    isLoading,
    error,
    updateTask: updateMutation.mutate,
    isUpdating: updateMutation.isLoading,
  }
}

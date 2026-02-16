import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { toast } from 'sonner'
import { tasksService } from '@/services/tasks.service'
import type { CreateTaskRequest, UpdateTaskRequest } from '@/types'

export function useTasks(filters?: {
  status?: string
  priority?: string
  search?: string
  ordering?: string
}) {
  const queryClient = useQueryClient()

  // Get all tasks with filters
  const { data, isLoading, error } = useQuery({
    queryKey: ['tasks', filters],
    queryFn: () => tasksService.getTasks(filters),
    staleTime: 30 * 1000, // 30 seconds
  })

  // Get task statistics
  const { data: statistics } = useQuery({
    queryKey: ['tasks', 'statistics'],
    queryFn: tasksService.getStatistics,
    staleTime: 60 * 1000, // 1 minute
  })

  // Create task mutation
  const createTaskMutation = useMutation({
    mutationFn: tasksService.createTask,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
      toast.success('Task created successfully')
    },
  })

  // Update task mutation
  const updateTaskMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: UpdateTaskRequest }) =>
      tasksService.updateTask(id, data),
    onMutate: async ({ id, data }) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ['tasks'] })

      // Snapshot previous value
      const previousTasks = queryClient.getQueryData(['tasks', filters])

      // Optimistically update
      queryClient.setQueryData(['tasks', filters], (old: any) => {
        if (!old?.results) return old
        return {
          ...old,
          results: old.results.map((task: any) =>
            task.id === id ? { ...task, ...data } : task
          ),
        }
      })

      return { previousTasks }
    },
    onError: (err, variables, context) => {
      // Rollback on error
      if (context?.previousTasks) {
        queryClient.setQueryData(['tasks', filters], context.previousTasks)
      }
      toast.error('Failed to update task')
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
      toast.success('Task updated successfully')
    },
  })

  // Delete task mutation
  const deleteTaskMutation = useMutation({
    mutationFn: tasksService.deleteTask,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
      toast.success('Task deleted successfully')
    },
  })

  // Restore task mutation
  const restoreTaskMutation = useMutation({
    mutationFn: tasksService.restoreTask,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
      toast.success('Task restored successfully')
    },
  })

  return {
    tasks: data?.results || [],
    totalCount: data?.count || 0,
    isLoading,
    error,
    statistics,
    createTask: createTaskMutation.mutate,
    isCreating: createTaskMutation.isPending,
    updateTask: updateTaskMutation.mutate,
    isUpdating: updateTaskMutation.isPending,
    deleteTask: deleteTaskMutation.mutate,
    isDeleting: deleteTaskMutation.isPending,
    restoreTask: restoreTaskMutation.mutate,
  }
}

export function useTask(id: number) {
  const queryClient = useQueryClient()

  const { data: task, isLoading } = useQuery({
    queryKey: ['tasks', id],
    queryFn: () => tasksService.getTask(id),
    enabled: !!id,
  })

  const { data: history } = useQuery({
    queryKey: ['tasks', id, 'history'],
    queryFn: () => tasksService.getTaskHistory(id),
    enabled: !!id,
  })

  return {
    task,
    history,
    isLoading,
  }
}

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { toast } from 'sonner'
import { tasksService } from '@/services/tasks.service'
import type { CreateTaskRequest, UpdateTaskRequest } from '@/types'

export function useTasks(params?: {
  status?: string
  priority?: string
  search?: string
  page?: number
  ordering?: string
}) {
  const queryClient = useQueryClient()

  const tasksQuery = useQuery({
    queryKey: ['tasks', params],
    queryFn: () => tasksService.getTasks(params),
  })

  const createTaskMutation = useMutation({
    mutationFn: (data: CreateTaskRequest) => tasksService.createTask(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
      toast.success('Task created successfully')
    },
  })

  const updateTaskMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: UpdateTaskRequest }) =>
      tasksService.updateTask(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
      toast.success('Task updated successfully')
    },
  })

  const deleteTaskMutation = useMutation({
    mutationFn: (id: number) => tasksService.deleteTask(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
      toast.success('Task deleted successfully')
    },
  })

  const restoreTaskMutation = useMutation({
    mutationFn: (id: number) => tasksService.restoreTask(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
      toast.success('Task restored successfully')
    },
  })

  return {
    tasks: tasksQuery.data?.results || [],
    count: tasksQuery.data?.count || 0,
    isLoading: tasksQuery.isLoading,
    error: tasksQuery.error,
    createTask: createTaskMutation.mutate,
    updateTask: updateTaskMutation.mutate,
    deleteTask: deleteTaskMutation.mutate,
    restoreTask: restoreTaskMutation.mutate,
    isCreating: createTaskMutation.isPending,
    isUpdating: updateTaskMutation.isPending,
    isDeleting: deleteTaskMutation.isPending,
    isRestoring: restoreTaskMutation.isPending,
  }
}

export function useTask(id: number) {
  const queryClient = useQueryClient()

  const taskQuery = useQuery({
    queryKey: ['task', id],
    queryFn: () => tasksService.getTask(id),
    enabled: !!id,
  })

  const historyQuery = useQuery({
    queryKey: ['task-history', id],
    queryFn: () => tasksService.getTaskHistory(id),
    enabled: !!id,
  })

  return {
    task: taskQuery.data,
    history: historyQuery.data || [],
    isLoading: taskQuery.isLoading,
    error: taskQuery.error,
  }
}

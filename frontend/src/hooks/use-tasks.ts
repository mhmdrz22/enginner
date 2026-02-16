import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { taskService } from '@/services/task-service'
import { toast } from 'sonner'
import type {
  CreateTaskRequest,
  UpdateTaskRequest,
  TaskStatus,
  TaskPriority,
} from '@/types'

interface UseTasksParams {
  status?: TaskStatus
  priority?: TaskPriority
  search?: string
  ordering?: string
  page?: number
}

export const useTasks = (params?: UseTasksParams) => {
  return useQuery({
    queryKey: ['tasks', params],
    queryFn: () => taskService.getTasks(params),
  })
}

export const useTask = (id: number) => {
  return useQuery({
    queryKey: ['tasks', id],
    queryFn: () => taskService.getTask(id),
    enabled: !!id,
  })
}

export const useTaskHistory = (taskId: number) => {
  return useQuery({
    queryKey: ['tasks', taskId, 'history'],
    queryFn: () => taskService.getTaskHistory(taskId),
    enabled: !!taskId,
  })
}

export const useTaskMutations = () => {
  const queryClient = useQueryClient()

  const createTask = useMutation({
    mutationFn: (data: CreateTaskRequest) => taskService.createTask(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
      toast.success('Task created successfully')
    },
  })

  const updateTask = useMutation({
    mutationFn: ({ id, data }: { id: number; data: UpdateTaskRequest }) =>
      taskService.updateTask(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
      toast.success('Task updated successfully')
    },
  })

  const deleteTask = useMutation({
    mutationFn: (id: number) => taskService.deleteTask(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
      toast.success('Task deleted successfully')
    },
  })

  const restoreTask = useMutation({
    mutationFn: (id: number) => taskService.restoreTask(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
      toast.success('Task restored successfully')
    },
  })

  const bulkUpdate = useMutation({
    mutationFn: ({ ids, data }: { ids: number[]; data: UpdateTaskRequest }) =>
      taskService.bulkUpdate(ids, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
      toast.success('Tasks updated successfully')
    },
  })

  const bulkDelete = useMutation({
    mutationFn: (ids: number[]) => taskService.bulkDelete(ids),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
      toast.success('Tasks deleted successfully')
    },
  })

  return {
    createTask,
    updateTask,
    deleteTask,
    restoreTask,
    bulkUpdate,
    bulkDelete,
  }
}

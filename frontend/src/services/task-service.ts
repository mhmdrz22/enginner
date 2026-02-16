import apiClient from '@/lib/api-client'
import type {
  Task,
  TaskHistory,
  CreateTaskRequest,
  UpdateTaskRequest,
  PaginatedResponse,
} from '@/types'

export const taskService = {
  // Get all tasks with optional filters
  getTasks: async (params?: {
    status?: string
    priority?: string
    search?: string
    ordering?: string
    page?: number
  }) => {
    const response = await apiClient.get<PaginatedResponse<Task>>('/tasks/', {
      params,
    })
    return response.data
  },

  // Get single task
  getTask: async (id: number) => {
    const response = await apiClient.get<Task>(`/tasks/${id}/`)
    return response.data
  },

  // Create task
  createTask: async (data: CreateTaskRequest) => {
    const response = await apiClient.post<Task>('/tasks/', data)
    return response.data
  },

  // Update task
  updateTask: async (id: number, data: UpdateTaskRequest) => {
    const response = await apiClient.patch<Task>(`/tasks/${id}/`, data)
    return response.data
  },

  // Delete task (soft delete)
  deleteTask: async (id: number) => {
    const response = await apiClient.delete(`/tasks/${id}/`)
    return response.data
  },

  // Restore deleted task
  restoreTask: async (id: number) => {
    const response = await apiClient.post<Task>(`/tasks/${id}/restore/`)
    return response.data
  },

  // Get task history
  getTaskHistory: async (taskId: number) => {
    const response = await apiClient.get<TaskHistory[]>(
      `/tasks/${taskId}/history/`
    )
    return response.data
  },

  // Bulk update tasks
  bulkUpdate: async (ids: number[], data: UpdateTaskRequest) => {
    const response = await apiClient.post('/tasks/bulk_update/', {
      task_ids: ids,
      data,
    })
    return response.data
  },

  // Bulk delete tasks
  bulkDelete: async (ids: number[]) => {
    const response = await apiClient.post('/tasks/bulk_delete/', {
      task_ids: ids,
    })
    return response.data
  },
}

import apiClient from '@/lib/api-client'
import type { Task, CreateTaskRequest, UpdateTaskRequest, PaginatedResponse, TaskHistory } from '@/types'

export const tasksService = {
  async getTasks(params?: {
    status?: string
    priority?: string
    search?: string
    ordering?: string
    page?: number
  }): Promise<PaginatedResponse<Task>> {
    const response = await apiClient.get<PaginatedResponse<Task>>('/tasks/', { params })
    return response.data
  },

  async getTask(id: number): Promise<Task> {
    const response = await apiClient.get<Task>(`/tasks/${id}/`)
    return response.data
  },

  async createTask(data: CreateTaskRequest): Promise<Task> {
    const response = await apiClient.post<Task>('/tasks/', data)
    return response.data
  },

  async updateTask(id: number, data: UpdateTaskRequest): Promise<Task> {
    const response = await apiClient.patch<Task>(`/tasks/${id}/`, data)
    return response.data
  },

  async deleteTask(id: number): Promise<void> {
    await apiClient.delete(`/tasks/${id}/`)
  },

  async restoreTask(id: number): Promise<Task> {
    const response = await apiClient.post<Task>(`/tasks/${id}/restore/`)
    return response.data
  },

  async getTaskHistory(id: number): Promise<TaskHistory[]> {
    const response = await apiClient.get<TaskHistory[]>(`/tasks/${id}/history/`)
    return response.data
  },

  async getStatistics(): Promise<{
    total: number
    by_status: Record<string, number>
    by_priority: Record<string, number>
    completed_this_week: number
  }> {
    const response = await apiClient.get('/tasks/statistics/')
    return response.data
  },
}

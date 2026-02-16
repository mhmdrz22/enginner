import apiClient from '@/lib/api-client'
import type { Task, CreateTaskRequest, UpdateTaskRequest, PaginatedResponse, TaskHistory } from '@/types'

export const tasksService = {
  async getTasks(params?: {
    status?: string
    priority?: string
    search?: string
    page?: number
    ordering?: string
  }): Promise<PaginatedResponse<Task>> {
    const response = await apiClient.get('/tasks/', { params })
    return response.data
  },

  async getTask(id: number): Promise<Task> {
    const response = await apiClient.get(`/tasks/${id}/`)
    return response.data
  },

  async createTask(data: CreateTaskRequest): Promise<Task> {
    const response = await apiClient.post('/tasks/', data)
    return response.data
  },

  async updateTask(id: number, data: UpdateTaskRequest): Promise<Task> {
    const response = await apiClient.patch(`/tasks/${id}/`, data)
    return response.data
  },

  async deleteTask(id: number): Promise<void> {
    await apiClient.delete(`/tasks/${id}/`)
  },

  async getTaskHistory(id: number): Promise<TaskHistory[]> {
    const response = await apiClient.get(`/tasks/${id}/history/`)
    return response.data
  },

  async restoreTask(id: number): Promise<Task> {
    const response = await apiClient.post(`/tasks/${id}/restore/`)
    return response.data
  },
}

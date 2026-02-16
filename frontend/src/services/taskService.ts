import api from '@/api'
import type { Task, TaskHistory, TaskFilters, PaginatedResponse } from '@/types'

export const taskService = {
  async getTasks(filters?: TaskFilters): Promise<Task[]> {
    const params = new URLSearchParams()
    if (filters?.search) params.append('search', filters.search)
    if (filters?.status) params.append('status', filters.status)
    if (filters?.priority) params.append('priority', filters.priority)
    if (filters?.assigned_to) params.append('assigned_to', filters.assigned_to.toString())
    if (filters?.created_by) params.append('created_by', filters.created_by.toString())

    const response = await api.get<PaginatedResponse<Task>>(
      `/tasks/?${params.toString()}`
    )
    return response.data.results || response.data
  },

  async getTask(id: number): Promise<Task> {
    const response = await api.get<Task>(`/tasks/${id}/`)
    return response.data
  },

  async createTask(data: Partial<Task>): Promise<Task> {
    const response = await api.post<Task>('/tasks/', data)
    return response.data
  },

  async updateTask(id: number, data: Partial<Task>): Promise<Task> {
    const response = await api.patch<Task>(`/tasks/${id}/`, data)
    return response.data
  },

  async deleteTask(id: number): Promise<void> {
    await api.delete(`/tasks/${id}/`)
  },

  async getTaskHistory(taskId: number): Promise<TaskHistory[]> {
    const response = await api.get<TaskHistory[]>(`/tasks/${taskId}/history/`)
    return response.data
  },

  async restoreTask(id: number): Promise<Task> {
    const response = await api.post<Task>(`/tasks/${id}/restore/`)
    return response.data
  },
}

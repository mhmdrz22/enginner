import api from '@/api'
import type { User, PaginatedResponse } from '@/types'

export const userService = {
  async getProfile(): Promise<User> {
    const response = await api.get<User>('/users/me/')
    return response.data
  },

  async updateProfile(data: Partial<User>): Promise<User> {
    const response = await api.patch<User>('/users/me/', data)
    return response.data
  },

  async getUsers(): Promise<User[]> {
    const response = await api.get<PaginatedResponse<User>>('/users/')
    return response.data.results || response.data
  },

  async getUser(id: number): Promise<User> {
    const response = await api.get<User>(`/users/${id}/`)
    return response.data
  },
}

import apiClient from '@/lib/api-client'
import type { LoginRequest, LoginResponse, RegisterRequest, User } from '@/types'

export const authService = {
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    const response = await apiClient.post<LoginResponse>('/accounts/login/', credentials)
    return response.data
  },

  async register(data: RegisterRequest): Promise<{ user: User; message: string }> {
    const response = await apiClient.post('/accounts/register/', data)
    return response.data
  },

  async logout(): Promise<void> {
    await apiClient.post('/accounts/logout/')
  },

  async getProfile(): Promise<User> {
    const response = await apiClient.get<User>('/accounts/profile/')
    return response.data
  },

  async updateProfile(data: Partial<User>): Promise<User> {
    const response = await apiClient.patch<User>('/accounts/profile/', data)
    return response.data
  },

  async refreshToken(refresh: string): Promise<{ access: string }> {
    const response = await apiClient.post('/accounts/token/refresh/', { refresh })
    return response.data
  },
}

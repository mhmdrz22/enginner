import api from '@/api'
import type { User, LoginRequest, LoginResponse, RegisterRequest } from '@/types'

export const authService = {
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    const response = await api.post<LoginResponse>('/auth/login/', credentials)
    return response.data
  },

  async register(data: RegisterRequest): Promise<User> {
    const response = await api.post<User>('/auth/register/', data)
    return response.data
  },

  async getProfile(): Promise<User> {
    const response = await api.get<User>('/users/me/')
    return response.data
  },

  async refreshToken(refresh: string): Promise<{ access: string }> {
    const response = await api.post<{ access: string }>('/auth/token/refresh/', {
      refresh,
    })
    return response.data
  },

  async requestPasswordReset(email: string): Promise<void> {
    await api.post('/auth/password-reset/', { email })
  },

  async resetPassword(token: string, password: string): Promise<void> {
    await api.post('/auth/password-reset/confirm/', { token, password })
  },
}

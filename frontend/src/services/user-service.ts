import apiClient from '@/lib/api-client'
import type {
  User,
  LoginRequest,
  LoginResponse,
  RegisterRequest,
} from '@/types'

export const userService = {
  // Authentication
  login: async (data: LoginRequest) => {
    const response = await apiClient.post<LoginResponse>(
      '/accounts/login/',
      data
    )
    return response.data
  },

  register: async (data: RegisterRequest) => {
    const response = await apiClient.post<{ user: User; message: string }>(
      '/accounts/register/',
      data
    )
    return response.data
  },

  logout: async () => {
    const response = await apiClient.post('/accounts/logout/')
    return response.data
  },

  // Profile
  getProfile: async () => {
    const response = await apiClient.get<User>('/accounts/profile/')
    return response.data
  },

  updateProfile: async (data: Partial<User>) => {
    const response = await apiClient.patch<User>('/accounts/profile/', data)
    return response.data
  },

  // Token refresh (handled by interceptor, but exposed for manual use)
  refreshToken: async (refreshToken: string) => {
    const response = await apiClient.post<{ access: string }>(
      '/accounts/token/refresh/',
      { refresh: refreshToken }
    )
    return response.data
  },
}

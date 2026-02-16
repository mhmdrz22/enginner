import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { userService } from '@/services/user-service'
import { useAuthStore } from '@/stores/auth-store'
import { toast } from 'sonner'
import type { LoginRequest, RegisterRequest } from '@/types'

export const useAuth = () => {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const { setUser, setTokens, logout: logoutStore } = useAuthStore()

  const login = useMutation({
    mutationFn: (data: LoginRequest) => userService.login(data),
    onSuccess: (data) => {
      setUser(data.user)
      setTokens(data.access, data.refresh)
      toast.success('Logged in successfully')
      navigate('/dashboard')
    },
  })

  const register = useMutation({
    mutationFn: (data: RegisterRequest) => userService.register(data),
    onSuccess: () => {
      toast.success('Registration successful! Please login.')
      navigate('/login')
    },
  })

  const logout = useMutation({
    mutationFn: () => userService.logout(),
    onSuccess: () => {
      logoutStore()
      queryClient.clear()
      toast.success('Logged out successfully')
      navigate('/login')
    },
    onError: () => {
      // Even if logout fails on server, clear client state
      logoutStore()
      queryClient.clear()
      navigate('/login')
    },
  })

  return {
    login,
    register,
    logout,
  }
}

export const useProfile = () => {
  const { user, isAuthenticated } = useAuthStore()

  return useQuery({
    queryKey: ['profile'],
    queryFn: () => userService.getProfile(),
    enabled: isAuthenticated,
    initialData: user || undefined,
  })
}

export const useUpdateProfile = () => {
  const queryClient = useQueryClient()
  const { setUser } = useAuthStore()

  return useMutation({
    mutationFn: (data: Partial<User>) => userService.updateProfile(data),
    onSuccess: (data) => {
      setUser(data)
      queryClient.invalidateQueries({ queryKey: ['profile'] })
      toast.success('Profile updated successfully')
    },
  })
}

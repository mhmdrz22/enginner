import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { toast } from 'sonner'
import { useAuthStore } from '@/stores/auth-store'
import { authService } from '@/services/auth.service'
import type { LoginRequest, RegisterRequest } from '@/types'

export function useAuth() {
  const queryClient = useQueryClient()
  const navigate = useNavigate()
  const { user, setUser, setTokens, logout: logoutStore } = useAuthStore()

  // Get current user profile
  const { data: profile, isLoading: isLoadingProfile } = useQuery({
    queryKey: ['profile'],
    queryFn: authService.getProfile,
    enabled: !!user,
    staleTime: 5 * 60 * 1000,
  })

  // Login mutation
  const loginMutation = useMutation({
    mutationFn: authService.login,
    onSuccess: (data) => {
      setTokens(data.access, data.refresh)
      setUser(data.user)
      queryClient.setQueryData(['profile'], data.user)
      toast.success('Welcome back!')
      navigate('/dashboard')
    },
    onError: () => {
      toast.error('Invalid email or password')
    },
  })

  // Register mutation
  const registerMutation = useMutation({
    mutationFn: authService.register,
    onSuccess: (data) => {
      toast.success(data.message || 'Registration successful! Please login.')
      navigate('/login')
    },
    onError: (error: any) => {
      const message = error.response?.data?.email?.[0] || 'Registration failed'
      toast.error(message)
    },
  })

  // Logout mutation
  const logoutMutation = useMutation({
    mutationFn: authService.logout,
    onSuccess: () => {
      logoutStore()
      queryClient.clear()
      toast.success('Logged out successfully')
      navigate('/login')
    },
  })

  // Update profile mutation
  const updateProfileMutation = useMutation({
    mutationFn: authService.updateProfile,
    onSuccess: (data) => {
      setUser(data)
      queryClient.setQueryData(['profile'], data)
      toast.success('Profile updated successfully')
    },
  })

  return {
    user: profile || user,
    isLoading: isLoadingProfile,
    login: loginMutation.mutate,
    isLoggingIn: loginMutation.isPending,
    register: registerMutation.mutate,
    isRegistering: registerMutation.isPending,
    logout: logoutMutation.mutate,
    updateProfile: updateProfileMutation.mutate,
    isUpdatingProfile: updateProfileMutation.isPending,
  }
}

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { toast } from 'sonner'
import { authService } from '@/services/auth.service'
import { useAuthStore } from '@/stores/auth-store'
import type { LoginRequest, RegisterRequest } from '@/types'

export function useAuth() {
  const queryClient = useQueryClient()
  const navigate = useNavigate()
  const { setUser, setTokens, logout: logoutStore } = useAuthStore()

  const loginMutation = useMutation({
    mutationFn: (data: LoginRequest) => authService.login(data),
    onSuccess: (data) => {
      setUser(data.user)
      setTokens(data.access, data.refresh)
      toast.success('Welcome back!')
      navigate('/dashboard')
    },
    onError: () => {
      toast.error('Invalid email or password')
    },
  })

  const registerMutation = useMutation({
    mutationFn: (data: RegisterRequest) => authService.register(data),
    onSuccess: (data) => {
      toast.success(data.message)
      navigate('/login')
    },
    onError: (error: any) => {
      const message = error.response?.data?.email?.[0] || 'Registration failed'
      toast.error(message)
    },
  })

  const logoutMutation = useMutation({
    mutationFn: () => authService.logout(),
    onSuccess: () => {
      logoutStore()
      queryClient.clear()
      toast.success('Logged out successfully')
      navigate('/login')
    },
  })

  const profileQuery = useQuery({
    queryKey: ['profile'],
    queryFn: () => authService.getProfile(),
    enabled: !!useAuthStore.getState().token,
  })

  const updateProfileMutation = useMutation({
    mutationFn: (data: Partial<any>) => authService.updateProfile(data),
    onSuccess: (data) => {
      setUser(data)
      queryClient.invalidateQueries({ queryKey: ['profile'] })
      toast.success('Profile updated successfully')
    },
  })

  return {
    login: loginMutation.mutate,
    register: registerMutation.mutate,
    logout: logoutMutation.mutate,
    updateProfile: updateProfileMutation.mutate,
    profile: profileQuery.data,
    isLoggingIn: loginMutation.isPending,
    isRegistering: registerMutation.isPending,
    isLoggingOut: logoutMutation.isPending,
    isUpdatingProfile: updateProfileMutation.isPending,
    isLoadingProfile: profileQuery.isLoading,
  }
}

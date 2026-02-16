import { useNavigate } from 'react-router-dom'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useAuthStore } from '@/stores/authStore'
import { authService } from '@/services/authService'
import { toast } from 'sonner'

export function useAuth() {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const { user, setUser, setTokens, clearAuth, isAuthenticated } = useAuthStore()

  const loginMutation = useMutation({
    mutationFn: authService.login,
    onSuccess: (data) => {
      setTokens(data.access, data.refresh)
      queryClient.invalidateQueries(['profile'])
      toast.success('Logged in successfully')
      navigate('/dashboard')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Login failed')
    },
  })

  const registerMutation = useMutation({
    mutationFn: authService.register,
    onSuccess: () => {
      toast.success('Account created successfully')
      navigate('/login')
    },
    onError: (error: any) => {
      const errors = error.response?.data
      if (errors) {
        Object.keys(errors).forEach((key) => {
          toast.error(`${key}: ${errors[key]}`)
        })
      } else {
        toast.error('Registration failed')
      }
    },
  })

  const { data: profile } = useQuery({
    queryKey: ['profile'],
    queryFn: authService.getProfile,
    enabled: isAuthenticated(),
    onSuccess: (data) => {
      setUser(data)
    },
    onError: () => {
      clearAuth()
    },
  })

  const logout = () => {
    clearAuth()
    queryClient.clear()
    toast.success('Logged out successfully')
    navigate('/login')
  }

  return {
    user: user || profile,
    isAuthenticated: isAuthenticated(),
    login: loginMutation.mutate,
    register: registerMutation.mutate,
    logout,
    isLoggingIn: loginMutation.isLoading,
    isRegistering: registerMutation.isLoading,
  }
}

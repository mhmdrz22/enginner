import { QueryClient } from '@tanstack/react-query'
import { toast } from 'sonner'
import type { AxiosError } from 'axios'
import type { ApiError } from '@/types'

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 5 * 60 * 1000, // 5 minutes
      gcTime: 10 * 60 * 1000, // 10 minutes (formerly cacheTime)
    },
    mutations: {
      onError: (error) => {
        const axiosError = error as AxiosError<ApiError>
        const message =
          axiosError.response?.data?.detail ||
          axiosError.response?.data?.message ||
          'An error occurred'
        toast.error(message)
      },
    },
  },
})

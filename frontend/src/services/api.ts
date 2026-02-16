import axios, { AxiosError } from 'axios';
import { useAuthStore } from '@/store/authStore';

// API Base URL
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - Add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - Handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as any;

    // If error is 401 and we haven't tried to refresh yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refreshToken');
        if (!refreshToken) {
          throw new Error('No refresh token');
        }

        // Try to refresh token
        const response = await axios.post(`${API_BASE_URL}/accounts/token/refresh/`, {
          refresh: refreshToken,
        });

        const { access } = response.data;
        localStorage.setItem('accessToken', access);

        // Retry original request
        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh failed - logout user
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        localStorage.removeItem('user');
        useAuthStore.getState().clearAuth();
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// ======================
// Authentication APIs
// ======================

export interface LoginResponse {
  access: string;
  refresh: string;
  user: {
    id: number;
    email: string;
    first_name: string;
    last_name: string;
    is_staff: boolean;
    is_superuser: boolean;
    is_active: boolean;
    is_verified: boolean;
    created_date: string;
    last_login_date?: string;
  };
}

export interface RegisterData {
  email: string;
  first_name: string;
  last_name: string;
  password: string;
}

export const register = (data: RegisterData) => {
  return api.post('/accounts/register/', data);
};

export const login = (email: string, password: string) => {
  return api.post<LoginResponse>('/accounts/login/', { email, password });
};

export const logout = () => {
  return api.post('/accounts/logout/');
};

export const refreshToken = (refresh: string) => {
  return api.post('/accounts/token/refresh/', { refresh });
};

export const fetchProfile = () => {
  return api.get('/accounts/profile/');
};

export const updateProfile = (data: { first_name: string; last_name: string; email: string }) => {
  return api.patch('/accounts/profile/', data);
};

// ======================
// Task APIs
// ======================

export interface Task {
  id: number;
  title: string;
  description: string;
  status: 'TODO' | 'DOING' | 'DONE';
  priority: 'LOW' | 'MEDIUM' | 'HIGH';
  due_date: string | null;
  tags: string;
  created_at: string;
  updated_at: string;
  completed_at: string | null;
  is_overdue: boolean;
  is_deleted: boolean;
  user: number;
}

export interface TaskCreateData {
  title: string;
  description?: string;
  status: 'TODO' | 'DOING' | 'DONE';
  priority: 'LOW' | 'MEDIUM' | 'HIGH';
  due_date?: string | null;
  tags?: string;
}

export interface TasksParams {
  status?: string;
  priority?: string;
  search?: string;
  ordering?: string;
  page?: number;
  page_size?: number;
}

export const fetchTasks = (params?: TasksParams) => {
  return api.get('/tasks/tasks/', { params });
};

export const fetchTask = (id: string | number) => {
  return api.get(`/tasks/tasks/${id}/`);
};

export const createTask = (data: TaskCreateData) => {
  return api.post('/tasks/tasks/', data);
};

export const updateTask = (id: string | number, data: Partial<TaskCreateData>) => {
  return api.patch(`/tasks/tasks/${id}/`, data);
};

export const deleteTask = (id: string | number) => {
  return api.delete(`/tasks/tasks/${id}/`);
};

export const restoreTask = (id: string | number) => {
  return api.post(`/tasks/tasks/${id}/restore/`);
};

export const fetchTaskHistory = (id: string | number) => {
  return api.get(`/tasks/tasks/${id}/history/`);
};

export const bulkUpdateTasks = (taskIds: number[], data: Partial<TaskCreateData>) => {
  return api.post('/tasks/tasks/bulk_update/', { task_ids: taskIds, data });
};

export const bulkDeleteTasks = (taskIds: number[]) => {
  return api.post('/tasks/tasks/bulk_delete/', { task_ids: taskIds });
};

// ======================
// Statistics APIs
// ======================

export interface TaskStatistics {
  total: number;
  by_status: {
    TODO: number;
    DOING: number;
    DONE: number;
  };
  by_priority: {
    LOW: number;
    MEDIUM: number;
    HIGH: number;
  };
  overdue: number;
}

export const fetchTaskStatistics = () => {
  return api.get<TaskStatistics>('/tasks/tasks/statistics/');
};

// ======================
// Helper Functions
// ======================

export const handleApiError = (error: any): string => {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<any>;
    
    // Network error
    if (!axiosError.response) {
      return 'خطا در اتصال به سرور. لطفا اتصال اینترنت خود را بررسی کنید.';
    }

    // Server error responses
    const status = axiosError.response.status;
    const data = axiosError.response.data;

    if (status === 400) {
      if (typeof data === 'object') {
        const firstError = Object.values(data)[0];
        if (Array.isArray(firstError)) {
          return firstError[0];
        }
        return firstError as string;
      }
      return data.detail || 'داده‌های ورودی نامعتبر است';
    }

    if (status === 401) {
      return 'لطفا وارد حساب کاربری خود شوید';
    }

    if (status === 403) {
      return 'شما اجازه دسترسی به این بخش را ندارید';
    }

    if (status === 404) {
      return 'اطلاعات مورد نظر یافت نشد';
    }

    if (status === 500) {
      return 'خطای سرور. لطفا بعدا تلاش کنید';
    }

    return data.detail || data.message || 'خطای غیرمنتظره رخ داده است';
  }

  return 'خطای غیرمنتظره رخ داده است';
};

export default api;

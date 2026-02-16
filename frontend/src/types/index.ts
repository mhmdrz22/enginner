// User types
export interface User {
  id: number
  email: string
  first_name: string
  last_name: string
  full_name: string
  is_active: boolean
  is_staff: boolean
  is_superuser: boolean
  is_verified: boolean
  created_date: string
  last_login_date: string | null
}

export interface LoginRequest {
  email: string
  password: string
}

export interface LoginResponse {
  access: string
  refresh: string
  user: User
}

export interface RegisterRequest {
  email: string
  first_name: string
  last_name: string
  password: string
  password2: string
}

// Task types
export type TaskStatus = 'TODO' | 'DOING' | 'DONE'
export type TaskPriority = 'LOW' | 'MEDIUM' | 'HIGH'

export interface Task {
  id: number
  title: string
  description: string
  status: TaskStatus
  priority: TaskPriority
  due_date: string | null
  tags: string
  completed_at: string | null
  is_deleted: boolean
  created_at: string
  updated_at: string
  user: number
}

export interface TaskHistory {
  id: number
  task: number
  field_name: string
  old_value: string
  new_value: string
  changed_at: string
  changed_by: number | null
}

export interface CreateTaskRequest {
  title: string
  description?: string
  status?: TaskStatus
  priority?: TaskPriority
  due_date?: string | null
  tags?: string
}

export interface UpdateTaskRequest extends Partial<CreateTaskRequest> {}

// API Response types
export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export interface ApiError {
  detail?: string
  message?: string
  [key: string]: any
}

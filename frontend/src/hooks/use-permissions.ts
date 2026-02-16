import { useAuthStore } from '@/stores/auth-store'
import type { User } from '@/types'

/**
 * Permission types
 */
export enum Permission {
  // Task permissions
  VIEW_TASKS = 'view_tasks',
  CREATE_TASKS = 'create_tasks',
  UPDATE_TASKS = 'update_tasks',
  DELETE_TASKS = 'delete_tasks',
  
  // User permissions
  VIEW_USERS = 'view_users',
  MANAGE_USERS = 'manage_users',
  
  // Admin permissions
  ACCESS_ADMIN = 'access_admin',
  MANAGE_SETTINGS = 'manage_settings',
}

/**
 * Role definitions with associated permissions
 */
const ROLE_PERMISSIONS: Record<string, Permission[]> = {
  user: [
    Permission.VIEW_TASKS,
    Permission.CREATE_TASKS,
    Permission.UPDATE_TASKS,
    Permission.DELETE_TASKS,
  ],
  staff: [
    Permission.VIEW_TASKS,
    Permission.CREATE_TASKS,
    Permission.UPDATE_TASKS,
    Permission.DELETE_TASKS,
    Permission.VIEW_USERS,
    Permission.ACCESS_ADMIN,
  ],
  superuser: [
    Permission.VIEW_TASKS,
    Permission.CREATE_TASKS,
    Permission.UPDATE_TASKS,
    Permission.DELETE_TASKS,
    Permission.VIEW_USERS,
    Permission.MANAGE_USERS,
    Permission.ACCESS_ADMIN,
    Permission.MANAGE_SETTINGS,
  ],
}

/**
 * Get user role based on user object
 */
function getUserRole(user: User | null): string {
  if (!user) return 'guest'
  if (user.is_superuser) return 'superuser'
  if (user.is_staff) return 'staff'
  return 'user'
}

/**
 * Get permissions for a specific role
 */
function getRolePermissions(role: string): Permission[] {
  return ROLE_PERMISSIONS[role] || []
}

/**
 * Hook for checking user permissions
 */
export function usePermissions() {
  const { user, isAuthenticated } = useAuthStore()

  /**
   * Check if user has a specific permission
   */
  const hasPermission = (permission: Permission): boolean => {
    if (!isAuthenticated || !user) return false

    const role = getUserRole(user)
    const permissions = getRolePermissions(role)

    return permissions.includes(permission)
  }

  /**
   * Check if user has ALL of the specified permissions
   */
  const hasAllPermissions = (permissions: Permission[]): boolean => {
    return permissions.every((permission) => hasPermission(permission))
  }

  /**
   * Check if user has ANY of the specified permissions
   */
  const hasAnyPermission = (permissions: Permission[]): boolean => {
    return permissions.some((permission) => hasPermission(permission))
  }

  /**
   * Check if user is admin (staff or superuser)
   */
  const isAdmin = (): boolean => {
    if (!user) return false
    return user.is_staff || user.is_superuser
  }

  /**
   * Check if user is superuser
   */
  const isSuperuser = (): boolean => {
    if (!user) return false
    return user.is_superuser
  }

  /**
   * Check if user can perform action on a resource
   * Resources can have ownership checks
   */
  const canAccess = (resourceOwnerId?: number): boolean => {
    if (!user) return false

    // Admins can access everything
    if (isAdmin()) return true

    // Users can access their own resources
    if (resourceOwnerId !== undefined) {
      return user.id === resourceOwnerId
    }

    // If no owner specified, just check authentication
    return isAuthenticated
  }

  return {
    hasPermission,
    hasAllPermissions,
    hasAnyPermission,
    isAdmin,
    isSuperuser,
    canAccess,
    user,
    isAuthenticated,
  }
}

/**
 * HOC for component-level permission checks
 */
export function withPermission<P extends object>(
  Component: React.ComponentType<P>,
  requiredPermission: Permission,
  fallback?: React.ReactNode
) {
  return function PermissionWrapper(props: P) {
    const { hasPermission } = usePermissions()

    if (!hasPermission(requiredPermission)) {
      return fallback ? <>{fallback}</> : null
    }

    return <Component {...props} />
  }
}

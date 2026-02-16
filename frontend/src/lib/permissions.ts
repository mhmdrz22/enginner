import type { User } from '@/types'
import { Permission } from '@/hooks/use-permissions'

/**
 * Utility functions for permission checks outside of React components
 */

/**
 * Check if user has a specific permission
 */
export function userHasPermission(user: User | null, permission: Permission): boolean {
  if (!user) return false

  // Superuser has all permissions
  if (user.is_superuser) return true

  // Staff has most permissions except user management
  if (user.is_staff) {
    const staffDenied = [Permission.MANAGE_USERS, Permission.MANAGE_SETTINGS]
    return !staffDenied.includes(permission)
  }

  // Regular users have basic task permissions
  const userPermissions = [
    Permission.VIEW_TASKS,
    Permission.CREATE_TASKS,
    Permission.UPDATE_TASKS,
    Permission.DELETE_TASKS,
  ]

  return userPermissions.includes(permission)
}

/**
 * Check if user can access admin panel
 */
export function canAccessAdmin(user: User | null): boolean {
  if (!user) return false
  return user.is_staff || user.is_superuser
}

/**
 * Check if user can manage other users
 */
export function canManageUsers(user: User | null): boolean {
  if (!user) return false
  return user.is_superuser
}

/**
 * Check if user owns a resource
 */
export function isResourceOwner(user: User | null, resourceOwnerId: number): boolean {
  if (!user) return false
  return user.id === resourceOwnerId
}

/**
 * Check if user can edit/delete a resource (owner or admin)
 */
export function canModifyResource(user: User | null, resourceOwnerId: number): boolean {
  if (!user) return false
  return isResourceOwner(user, resourceOwnerId) || canAccessAdmin(user)
}

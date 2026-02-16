import { usePermissions, Permission } from '@/hooks/use-permissions'

interface PermissionGuardProps {
  children: React.ReactNode
  permission?: Permission
  permissions?: Permission[]
  requireAll?: boolean
  fallback?: React.ReactNode
}

/**
 * Component-level permission guard
 * Shows children only if user has required permissions
 * 
 * @param permission - Single permission to check
 * @param permissions - Multiple permissions to check
 * @param requireAll - If true, user must have ALL permissions. If false, user needs ANY permission (default: false)
 * @param fallback - What to show if user doesn't have permission (default: null)
 */
export function PermissionGuard({
  children,
  permission,
  permissions,
  requireAll = false,
  fallback = null,
}: PermissionGuardProps) {
  const { hasPermission, hasAllPermissions, hasAnyPermission } = usePermissions()

  // Single permission check
  if (permission) {
    if (!hasPermission(permission)) {
      return <>{fallback}</>
    }
    return <>{children}</>
  }

  // Multiple permissions check
  if (permissions && permissions.length > 0) {
    const hasAccess = requireAll
      ? hasAllPermissions(permissions)
      : hasAnyPermission(permissions)

    if (!hasAccess) {
      return <>{fallback}</>
    }
    return <>{children}</>
  }

  // No permission specified, show children
  return <>{children}</>
}

/**
 * Admin-only guard
 */
export function AdminGuard({
  children,
  fallback = null,
}: {
  children: React.ReactNode
  fallback?: React.ReactNode
}) {
  const { isAdmin } = usePermissions()

  if (!isAdmin()) {
    return <>{fallback}</>
  }

  return <>{children}</>
}

/**
 * Resource ownership guard
 * Shows content only if user owns the resource or is admin
 */
export function OwnershipGuard({
  children,
  resourceOwnerId,
  fallback = null,
}: {
  children: React.ReactNode
  resourceOwnerId: number
  fallback?: React.ReactNode
}) {
  const { canAccess } = usePermissions()

  if (!canAccess(resourceOwnerId)) {
    return <>{fallback}</>
  }

  return <>{children}</>
}

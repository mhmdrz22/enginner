import { Navigate, useLocation } from 'react-router-dom'
import { useAuthStore } from '@/stores/auth-store'

interface ProtectedRouteProps {
  children: React.ReactNode
  requireAuth?: boolean
  requireAdmin?: boolean
  redirectTo?: string
}

/**
 * Protected Route Component
 * Wraps routes that require authentication or specific permissions
 * 
 * @param children - Child components to render if authorized
 * @param requireAuth - Whether authentication is required (default: true)
 * @param requireAdmin - Whether admin privileges are required (default: false)
 * @param redirectTo - Where to redirect if not authorized (default: /login)
 */
export function ProtectedRoute({
  children,
  requireAuth = true,
  requireAdmin = false,
  redirectTo = '/login',
}: ProtectedRouteProps) {
  const { isAuthenticated, user } = useAuthStore()
  const location = useLocation()

  // Check authentication
  if (requireAuth && !isAuthenticated) {
    // Redirect to login, but save the current location for redirecting back after login
    return <Navigate to={redirectTo} state={{ from: location }} replace />
  }

  // Check admin privileges
  if (requireAdmin && (!user?.is_staff && !user?.is_superuser)) {
    // Redirect to dashboard if user is authenticated but not an admin
    return <Navigate to="/dashboard" replace />
  }

  // User is authorized, render children
  return <>{children}</>
}

/**
 * Convenience wrapper for private routes (requires authentication)
 */
export function PrivateRoute({ children }: { children: React.ReactNode }) {
  return (
    <ProtectedRoute requireAuth={true} requireAdmin={false}>
      {children}
    </ProtectedRoute>
  )
}

/**
 * Convenience wrapper for admin-only routes
 */
export function AdminRoute({ children }: { children: React.ReactNode }) {
  return (
    <ProtectedRoute requireAuth={true} requireAdmin={true}>
      {children}
    </ProtectedRoute>
  )
}

/**
 * Public route that redirects authenticated users to dashboard
 * Useful for login/register pages
 */
export function PublicRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuthStore()

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />
  }

  return <>{children}</>
}

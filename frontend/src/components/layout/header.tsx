import { Bell } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { MobileNav } from './mobile-nav'
import { ThemeToggle } from './theme-toggle'
import { UserAvatar } from './user-avatar'
import { useAuthStore } from '@/stores/auth-store'

export function Header() {
  const { user } = useAuthStore()

  return (
    <header className="sticky top-0 z-30 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between px-4">
        {/* Mobile Nav */}
        <div className="flex items-center gap-4">
          <MobileNav />
          <h1 className="text-xl font-bold lg:hidden">
            TaskBoard
          </h1>
        </div>

        {/* Right Section */}
        <div className="flex items-center gap-2">
          {/* Notifications */}
          <Button variant="ghost" size="icon" className="relative">
            <Bell className="h-5 w-5" />
            <span className="absolute top-1 right-1 w-2 h-2 bg-destructive rounded-full" />
            <span className="sr-only">Notifications</span>
          </Button>

          {/* Theme Toggle */}
          <ThemeToggle />

          {/* User Avatar */}
          <UserAvatar user={user} />
        </div>
      </div>
    </header>
  )
}

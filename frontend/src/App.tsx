import { useEffect } from 'react'
import { BrowserRouter } from 'react-router-dom'
import { QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { Toaster } from '@/components/ui/toaster'
import { queryClient } from '@/lib/query-client'
import { useUIStore } from '@/stores/ui-store'

function App() {
  const { theme, setTheme } = useUIStore()

  // Initialize theme on mount
  useEffect(() => {
    setTheme(theme)
  }, [])

  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div className="min-h-screen bg-background text-foreground">
          {/* TODO: Add Router with pages */}
          <div className="container mx-auto p-8">
            <h1 className="text-4xl font-bold mb-4">TaskBoard Application</h1>
            <p className="text-muted-foreground">
              Frontend is ready! Pages will be added next.
            </p>
            <div className="mt-8 space-y-4">
              <h2 className="text-2xl font-semibold">Features Implemented:</h2>
              <ul className="list-disc list-inside space-y-2 text-muted-foreground">
                <li>✅ Modern UI with shadcn/ui components</li>
                <li>✅ React Query for data fetching</li>
                <li>✅ Zustand for state management</li>
                <li>✅ TypeScript types</li>
                <li>✅ API client with JWT auth</li>
                <li>✅ Kanban board component</li>
                <li>✅ Task filters & search</li>
                <li>✅ Task history viewer</li>
                <li>✅ Dark mode support</li>
                <li>✅ Responsive navigation</li>
                <li>✅ Mobile menu</li>
                <li>✅ User avatar & dropdown</li>
                <li>✅ Notification bell</li>
                <li>✅ Drag & drop ready</li>
              </ul>
            </div>
          </div>
        </div>
        <Toaster />
      </BrowserRouter>
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  )
}

export default App

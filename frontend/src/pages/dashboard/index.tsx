import { useState } from 'react'
import { Plus, Search } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { TaskBoard } from '@/components/tasks/task-board'
import { CreateTaskDialog } from '@/components/tasks/create-task-dialog'
import { DashboardLayout } from '@/components/layout/dashboard-layout'

export function DashboardPage() {
  const [status, setStatus] = useState<string>('')
  const [priority, setPriority] = useState<string>('')
  const [search, setSearch] = useState('')
  const [isCreateOpen, setIsCreateOpen] = useState(false)

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">My Tasks</h1>
            <p className="text-muted-foreground">
              Manage your tasks and track your progress
            </p>
          </div>
          <Button onClick={() => setIsCreateOpen(true)}>
            <Plus className="mr-2 h-4 w-4" />
            New Task
          </Button>
        </div>

        {/* Filters */}
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search tasks..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-10"
            />
          </div>
          <Select value={status} onValueChange={setStatus}>
            <SelectTrigger className="w-full sm:w-[180px]">
              <SelectValue placeholder="All statuses" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All statuses</SelectItem>
              <SelectItem value="TODO">To Do</SelectItem>
              <SelectItem value="DOING">In Progress</SelectItem>
              <SelectItem value="DONE">Done</SelectItem>
            </SelectContent>
          </Select>
          <Select value={priority} onValueChange={setPriority}>
            <SelectTrigger className="w-full sm:w-[180px]">
              <SelectValue placeholder="All priorities" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All priorities</SelectItem>
              <SelectItem value="HIGH">High</SelectItem>
              <SelectItem value="MEDIUM">Medium</SelectItem>
              <SelectItem value="LOW">Low</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* Task Board */}
        <TaskBoard
          status={status === 'all' ? undefined : status}
          priority={priority === 'all' ? undefined : priority}
          search={search}
        />
      </div>

      <CreateTaskDialog open={isCreateOpen} onOpenChange={setIsCreateOpen} />
    </DashboardLayout>
  )
}

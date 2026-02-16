import { useTasks } from '@/hooks/use-tasks'
import { TaskCard } from './task-card'
import { Loader2 } from 'lucide-react'
import type { TaskStatus } from '@/types'

interface TaskBoardProps {
  status?: string
  priority?: string
  search?: string
}

export function TaskBoard({ status, priority, search }: TaskBoardProps) {
  const { tasks, isLoading } = useTasks({ status, priority, search })

  const columns: { status: TaskStatus; title: string; color: string }[] = [
    { status: 'TODO', title: 'To Do', color: 'bg-gray-100 dark:bg-gray-800' },
    { status: 'DOING', title: 'In Progress', color: 'bg-blue-100 dark:bg-blue-900' },
    { status: 'DONE', title: 'Done', color: 'bg-green-100 dark:bg-green-900' },
  ]

  const getTasksByStatus = (taskStatus: TaskStatus) => {
    return tasks.filter((task) => task.status === taskStatus)
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {columns.map((column) => {
        const columnTasks = getTasksByStatus(column.status)
        
        return (
          <div key={column.status} className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="font-semibold text-lg">{column.title}</h3>
              <span className="text-sm text-muted-foreground">
                {columnTasks.length}
              </span>
            </div>
            <div className={`rounded-lg p-4 min-h-[500px] ${column.color}`}>
              <div className="space-y-3">
                {columnTasks.map((task) => (
                  <TaskCard key={task.id} task={task} />
                ))}
                {columnTasks.length === 0 && (
                  <p className="text-sm text-center text-muted-foreground py-8">
                    No tasks
                  </p>
                )}
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}

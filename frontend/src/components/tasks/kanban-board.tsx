import { useState } from 'react'
import { useTasks, useTaskMutations } from '@/hooks/use-tasks'
import { TaskCard } from './task-card'
import { TaskFilters } from './task-filters'
import { TaskSearch } from './task-search'
import { Button } from '@/components/ui/button'
import { Plus } from 'lucide-react'
import type { TaskStatus, TaskPriority } from '@/types'

const COLUMNS: { id: TaskStatus; title: string; bgColor: string }[] = [
  { id: 'TODO', title: 'To Do', bgColor: 'bg-slate-100 dark:bg-slate-800' },
  { id: 'DOING', title: 'In Progress', bgColor: 'bg-blue-50 dark:bg-blue-900/20' },
  { id: 'DONE', title: 'Done', bgColor: 'bg-green-50 dark:bg-green-900/20' },
]

interface KanbanBoardProps {
  onCreateTask: () => void
  onEditTask: (taskId: number) => void
}

export function KanbanBoard({ onCreateTask, onEditTask }: KanbanBoardProps) {
  const [status, setStatus] = useState<TaskStatus | undefined>()
  const [priority, setPriority] = useState<TaskPriority | undefined>()
  const [search, setSearch] = useState('')
  const [ordering, setOrdering] = useState('-created_at')

  const { data, isLoading } = useTasks({
    status,
    priority,
    search,
    ordering,
  })
  const { updateTask } = useTaskMutations()

  const tasks = data?.results || []

  const handleDragStart = (e: React.DragEvent, taskId: number) => {
    e.dataTransfer.setData('taskId', taskId.toString())
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
  }

  const handleDrop = (e: React.DragEvent, newStatus: TaskStatus) => {
    e.preventDefault()
    const taskId = parseInt(e.dataTransfer.getData('taskId'))
    const task = tasks.find((t) => t.id === taskId)

    if (task && task.status !== newStatus) {
      updateTask.mutate({
        id: taskId,
        data: { status: newStatus },
      })
    }
  }

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="flex flex-col sm:flex-row gap-4 mb-6">
        <div className="flex-1">
          <TaskSearch value={search} onChange={setSearch} />
        </div>
        <TaskFilters
          status={status}
          priority={priority}
          ordering={ordering}
          onStatusChange={setStatus}
          onPriorityChange={setPriority}
          onOrderingChange={setOrdering}
        />
        <Button onClick={onCreateTask}>
          <Plus className="w-4 h-4 mr-2" />
          New Task
        </Button>
      </div>

      {/* Kanban Board */}
      <div className="flex-1 overflow-x-auto">
        <div className="flex gap-4 h-full min-w-max pb-4">
          {COLUMNS.map((column) => {
            const columnTasks = tasks.filter((task) => task.status === column.id && !task.is_deleted)

            return (
              <div
                key={column.id}
                className="flex-1 min-w-[300px] flex flex-col"
                onDragOver={handleDragOver}
                onDrop={(e) => handleDrop(e, column.id)}
              >
                {/* Column Header */}
                <div className={`rounded-t-lg p-4 ${column.bgColor}`}>
                  <div className="flex items-center justify-between">
                    <h3 className="font-semibold text-lg">{column.title}</h3>
                    <span className="text-sm text-muted-foreground">
                      {columnTasks.length}
                    </span>
                  </div>
                </div>

                {/* Column Content */}
                <div className="flex-1 border border-t-0 rounded-b-lg p-4 bg-muted/20 min-h-[500px] overflow-y-auto">
                  {isLoading ? (
                    <div className="flex items-center justify-center h-32">
                      <p className="text-muted-foreground">Loading...</p>
                    </div>
                  ) : columnTasks.length === 0 ? (
                    <div className="flex items-center justify-center h-32">
                      <p className="text-muted-foreground text-sm">
                        No tasks
                      </p>
                    </div>
                  ) : (
                    <div className="space-y-3">
                      {columnTasks.map((task) => (
                        <div
                          key={task.id}
                          draggable
                          onDragStart={(e) => handleDragStart(e, task.id)}
                          className="cursor-move"
                        >
                          <TaskCard
                            task={task}
                            onClick={() => onEditTask(task.id)}
                          />
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}

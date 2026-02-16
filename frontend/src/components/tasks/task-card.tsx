import { formatDate } from '@/lib/utils'
import { Card, CardContent, CardFooter, CardHeader } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Clock, Edit, Trash2 } from 'lucide-react'
import type { Task } from '@/types'

interface TaskCardProps {
  task: Task
  onEdit?: (task: Task) => void
  onDelete?: (id: number) => void
}

const priorityColors = {
  LOW: 'secondary',
  MEDIUM: 'warning',
  HIGH: 'destructive',
} as const

const statusColors = {
  TODO: 'outline',
  DOING: 'info',
  DONE: 'success',
} as const

export function TaskCard({ task, onEdit, onDelete }: TaskCardProps) {
  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between gap-2">
          <h3 className="font-semibold text-lg line-clamp-2">{task.title}</h3>
          <div className="flex gap-1">
            {onEdit && (
              <Button
                variant="ghost"
                size="icon"
                className="h-8 w-8"
                onClick={() => onEdit(task)}
              >
                <Edit className="h-4 w-4" />
              </Button>
            )}
            {onDelete && (
              <Button
                variant="ghost"
                size="icon"
                className="h-8 w-8 text-destructive"
                onClick={() => onDelete(task.id)}
              >
                <Trash2 className="h-4 w-4" />
              </Button>
            )}
          </div>
        </div>
        <div className="flex gap-2 mt-2">
          <Badge variant={statusColors[task.status]}>
            {task.status}
          </Badge>
          <Badge variant={priorityColors[task.priority]}>
            {task.priority}
          </Badge>
        </div>
      </CardHeader>
      {task.description && (
        <CardContent className="pb-3">
          <p className="text-sm text-muted-foreground line-clamp-3">
            {task.description}
          </p>
        </CardContent>
      )}
      <CardFooter className="pt-0">
        <div className="flex items-center gap-4 text-sm text-muted-foreground">
          {task.due_date && (
            <div className="flex items-center gap-1">
              <Clock className="h-4 w-4" />
              <span>{formatDate(task.due_date)}</span>
            </div>
          )}
          {task.tags && (
            <div className="flex gap-1 flex-wrap">
              {task.tags.split(',').filter(Boolean).map((tag) => (
                <span
                  key={tag}
                  className="px-2 py-0.5 text-xs bg-secondary rounded"
                >
                  {tag.trim()}
                </span>
              ))}
            </div>
          )}
        </div>
      </CardFooter>
    </Card>
  )
}

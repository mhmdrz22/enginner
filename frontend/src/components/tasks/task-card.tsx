import { Card, CardContent, CardHeader } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Calendar, Clock } from 'lucide-react'
import { formatDate } from '@/lib/utils'
import type { Task } from '@/types'

interface TaskCardProps {
  task: Task
  onClick: () => void
}

const PRIORITY_COLORS = {
  LOW: 'default',
  MEDIUM: 'warning',
  HIGH: 'destructive',
} as const

const PRIORITY_LABELS = {
  LOW: 'Low',
  MEDIUM: 'Medium',
  HIGH: 'High',
}

export function TaskCard({ task, onClick }: TaskCardProps) {
  const isDue = task.due_date && new Date(task.due_date) < new Date()
  const tags = task.tags ? task.tags.split(',').filter(Boolean) : []

  return (
    <Card
      className="cursor-pointer hover:shadow-md transition-shadow"
      onClick={onClick}
    >
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between gap-2">
          <h4 className="font-medium line-clamp-2">{task.title}</h4>
          <Badge variant={PRIORITY_COLORS[task.priority]} className="shrink-0">
            {PRIORITY_LABELS[task.priority]}
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="space-y-3">
        {task.description && (
          <p className="text-sm text-muted-foreground line-clamp-2">
            {task.description}
          </p>
        )}

        {/* Tags */}
        {tags.length > 0 && (
          <div className="flex flex-wrap gap-1">
            {tags.slice(0, 3).map((tag, index) => (
              <Badge key={index} variant="outline" className="text-xs">
                {tag.trim()}
              </Badge>
            ))}
            {tags.length > 3 && (
              <Badge variant="outline" className="text-xs">
                +{tags.length - 3}
              </Badge>
            )}
          </div>
        )}

        {/* Due Date */}
        {task.due_date && (
          <div className="flex items-center gap-1 text-xs">
            <Calendar className="w-3 h-3" />
            <span className={isDue ? 'text-destructive font-medium' : 'text-muted-foreground'}>
              {formatDate(task.due_date)}
              {isDue && ' (Overdue)'}
            </span>
          </div>
        )}

        {/* Created Date */}
        <div className="flex items-center gap-1 text-xs text-muted-foreground">
          <Clock className="w-3 h-3" />
          <span>Created {formatDate(task.created_at)}</span>
        </div>
      </CardContent>
    </Card>
  )
}

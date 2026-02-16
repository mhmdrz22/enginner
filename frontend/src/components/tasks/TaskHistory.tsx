import { Clock, User } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { formatDate } from '@/lib/utils'
import type { TaskHistory as TaskHistoryType } from '@/types'

interface TaskHistoryProps {
  taskId: number
  history: TaskHistoryType[]
}

export default function TaskHistory({ history }: TaskHistoryProps) {
  if (!history || history.length === 0) {
    return (
      <Card>
        <CardContent className="flex items-center justify-center p-12">
          <p className="text-muted-foreground">No history available</p>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Task History</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {history.map((entry, index) => (
            <div
              key={entry.id || index}
              className="flex gap-4 border-b pb-4 last:border-b-0 last:pb-0"
            >
              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary/10">
                <Clock className="h-4 w-4 text-primary" />
              </div>
              <div className="flex-1 space-y-1">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="font-medium">{entry.action}</span>
                    {entry.field && (
                      <Badge variant="outline" className="text-xs">
                        {entry.field}
                      </Badge>
                    )}
                  </div>
                  <span className="text-xs text-muted-foreground">
                    {formatDate(entry.timestamp)}
                  </span>
                </div>
                {entry.old_value && entry.new_value && (
                  <div className="text-sm text-muted-foreground">
                    <span className="line-through">{entry.old_value}</span>
                    {' → '}
                    <span className="text-foreground">{entry.new_value}</span>
                  </div>
                )}
                {entry.user && (
                  <div className="flex items-center gap-1 text-xs text-muted-foreground">
                    <User className="h-3 w-3" />
                    <span>{entry.user.email}</span>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}

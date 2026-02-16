import { useTaskHistory } from '@/hooks/use-tasks'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Badge } from '@/components/ui/badge'
import { formatDateTime } from '@/lib/utils'
import { Clock, User } from 'lucide-react'

interface TaskHistoryDialogProps {
  taskId: number
  open: boolean
  onOpenChange: (open: boolean) => void
}

const FIELD_LABELS: Record<string, string> = {
  title: 'Title',
  description: 'Description',
  status: 'Status',
  priority: 'Priority',
  due_date: 'Due Date',
  tags: 'Tags',
}

export function TaskHistoryDialog({
  taskId,
  open,
  onOpenChange,
}: TaskHistoryDialogProps) {
  const { data: history, isLoading } = useTaskHistory(taskId)

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl max-h-[600px] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Task History</DialogTitle>
        </DialogHeader>

        <div className="space-y-4 mt-4">
          {isLoading ? (
            <div className="text-center py-8 text-muted-foreground">
              Loading history...
            </div>
          ) : !history || history.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground">
              No history available
            </div>
          ) : (
            history.map((entry) => (
              <div
                key={entry.id}
                className="border-l-2 border-muted pl-4 py-2 relative"
              >
                {/* Timeline dot */}
                <div className="absolute left-[-5px] top-3 w-2 h-2 rounded-full bg-primary" />

                {/* Change info */}
                <div className="space-y-2">
                  <div className="flex items-center gap-2 text-sm">
                    <Badge variant="outline">
                      {FIELD_LABELS[entry.field_name] || entry.field_name}
                    </Badge>
                    <span className="text-muted-foreground">changed</span>
                  </div>

                  {/* Old -> New values */}
                  <div className="flex items-center gap-2 text-sm">
                    {entry.old_value && (
                      <>
                        <code className="px-2 py-1 bg-muted rounded text-xs">
                          {entry.old_value}
                        </code>
                        <span className="text-muted-foreground">→</span>
                      </>
                    )}
                    <code className="px-2 py-1 bg-primary/10 rounded text-xs">
                      {entry.new_value}
                    </code>
                  </div>

                  {/* Metadata */}
                  <div className="flex flex-wrap items-center gap-4 text-xs text-muted-foreground">
                    <div className="flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      <span>{formatDateTime(entry.changed_at)}</span>
                    </div>
                    {entry.changed_by && (
                      <div className="flex items-center gap-1">
                        <User className="w-3 h-3" />
                        <span>User #{entry.changed_by}</span>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </DialogContent>
    </Dialog>
  )
}

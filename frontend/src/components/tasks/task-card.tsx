import { useState } from 'react'
import { Calendar, MoreVertical, Trash2, Edit } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { formatDate } from '@/lib/utils'
import { useTasks } from '@/hooks/use-tasks'
import { EditTaskDialog } from './edit-task-dialog'
import type { Task } from '@/types'

interface TaskCardProps {
  task: Task
}

export function TaskCard({ task }: TaskCardProps) {
  const { deleteTask, isDeleting } = useTasks()
  const [showDeleteDialog, setShowDeleteDialog] = useState(false)
  const [showEditDialog, setShowEditDialog] = useState(false)

  const priorityColors = {
    HIGH: 'destructive',
    MEDIUM: 'warning',
    LOW: 'secondary',
  } as const

  const handleDelete = () => {
    deleteTask(task.id)
    setShowDeleteDialog(false)
  }

  return (
    <>
      <Card className="cursor-pointer hover:shadow-md transition-shadow">
        <CardHeader className="pb-3">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <CardTitle className="text-base line-clamp-2">{task.title}</CardTitle>
              {task.due_date && (
                <CardDescription className="flex items-center gap-1 mt-2">
                  <Calendar className="h-3 w-3" />
                  {formatDate(task.due_date)}
                </CardDescription>
              )}
            </div>
            <div className="flex gap-1">
              <Button
                variant="ghost"
                size="icon"
                className="h-8 w-8"
                onClick={() => setShowEditDialog(true)}
              >
                <Edit className="h-4 w-4" />
              </Button>
              <Button
                variant="ghost"
                size="icon"
                className="h-8 w-8"
                onClick={() => setShowDeleteDialog(true)}
              >
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </CardHeader>
        {task.description && (
          <CardContent className="pt-0">
            <p className="text-sm text-muted-foreground line-clamp-3">
              {task.description}
            </p>
            <div className="mt-3">
              <Badge variant={priorityColors[task.priority]}>
                {task.priority}
              </Badge>
            </div>
          </CardContent>
        )}
      </Card>

      {/* Delete Confirmation Dialog */}
      <Dialog open={showDeleteDialog} onOpenChange={setShowDeleteDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Delete Task</DialogTitle>
            <DialogDescription>
              Are you sure you want to delete this task? This action cannot be undone.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowDeleteDialog(false)}>
              Cancel
            </Button>
            <Button
              variant="destructive"
              onClick={handleDelete}
              disabled={isDeleting}
            >
              Delete
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Edit Dialog */}
      <EditTaskDialog
        task={task}
        open={showEditDialog}
        onOpenChange={setShowEditDialog}
      />
    </>
  )
}

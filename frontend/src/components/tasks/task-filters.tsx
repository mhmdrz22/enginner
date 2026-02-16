import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Button } from '@/components/ui/button'
import { X } from 'lucide-react'
import type { TaskStatus, TaskPriority } from '@/types'

interface TaskFiltersProps {
  status?: TaskStatus
  priority?: TaskPriority
  ordering: string
  onStatusChange: (status: TaskStatus | undefined) => void
  onPriorityChange: (priority: TaskPriority | undefined) => void
  onOrderingChange: (ordering: string) => void
}

export function TaskFilters({
  status,
  priority,
  ordering,
  onStatusChange,
  onPriorityChange,
  onOrderingChange,
}: TaskFiltersProps) {
  const hasFilters = status || priority || ordering !== '-created_at'

  const clearFilters = () => {
    onStatusChange(undefined)
    onPriorityChange(undefined)
    onOrderingChange('-created_at')
  }

  return (
    <div className="flex flex-wrap items-center gap-2">
      {/* Status Filter */}
      <Select
        value={status || 'all'}
        onValueChange={(value) =>
          onStatusChange(value === 'all' ? undefined : (value as TaskStatus))
        }
      >
        <SelectTrigger className="w-[140px]">
          <SelectValue placeholder="Status" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">All Status</SelectItem>
          <SelectItem value="TODO">To Do</SelectItem>
          <SelectItem value="DOING">In Progress</SelectItem>
          <SelectItem value="DONE">Done</SelectItem>
        </SelectContent>
      </Select>

      {/* Priority Filter */}
      <Select
        value={priority || 'all'}
        onValueChange={(value) =>
          onPriorityChange(
            value === 'all' ? undefined : (value as TaskPriority)
          )
        }
      >
        <SelectTrigger className="w-[140px]">
          <SelectValue placeholder="Priority" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">All Priority</SelectItem>
          <SelectItem value="LOW">Low</SelectItem>
          <SelectItem value="MEDIUM">Medium</SelectItem>
          <SelectItem value="HIGH">High</SelectItem>
        </SelectContent>
      </Select>

      {/* Sort */}
      <Select value={ordering} onValueChange={onOrderingChange}>
        <SelectTrigger className="w-[160px]">
          <SelectValue placeholder="Sort by" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="-created_at">Newest First</SelectItem>
          <SelectItem value="created_at">Oldest First</SelectItem>
          <SelectItem value="-updated_at">Recently Updated</SelectItem>
          <SelectItem value="due_date">Due Date</SelectItem>
          <SelectItem value="-priority">Priority (High to Low)</SelectItem>
          <SelectItem value="priority">Priority (Low to High)</SelectItem>
          <SelectItem value="title">Title (A-Z)</SelectItem>
          <SelectItem value="-title">Title (Z-A)</SelectItem>
        </SelectContent>
      </Select>

      {/* Clear Filters */}
      {hasFilters && (
        <Button
          variant="ghost"
          size="sm"
          onClick={clearFilters}
          className="h-10"
        >
          <X className="w-4 h-4 mr-1" />
          Clear
        </Button>
      )}
    </div>
  )
}

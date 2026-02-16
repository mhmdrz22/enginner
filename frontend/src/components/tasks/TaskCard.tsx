import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { Link } from 'react-router-dom';
import {
  Calendar,
  Clock,
  MoreVertical,
  Trash2,
  Edit,
  Eye,
  AlertCircle,
} from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { format } from 'date-fns';
import { faIR } from 'date-fns/locale';

interface TaskCardProps {
  task: any;
  onDelete?: () => void;
  onEdit?: () => void;
  isDragging?: boolean;
}

export default function TaskCard({ task, onDelete, onEdit, isDragging }: TaskCardProps) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging: isSortableDragging,
  } = useSortable({
    id: task.id.toString(),
  });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isSortableDragging ? 0.5 : 1,
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'HIGH':
        return 'border-l-4 border-l-red-500';
      case 'MEDIUM':
        return 'border-l-4 border-l-yellow-500';
      case 'LOW':
        return 'border-l-4 border-l-green-500';
      default:
        return 'border-l-4 border-l-gray-300';
    }
  };

  const getPriorityBadge = (priority: string) => {
    switch (priority) {
      case 'HIGH':
        return (
          <Badge className="bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200 text-xs">
            بالا
          </Badge>
        );
      case 'MEDIUM':
        return (
          <Badge className="bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200 text-xs">
            متوسط
          </Badge>
        );
      case 'LOW':
        return (
          <Badge className="bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200 text-xs">
            پایین
          </Badge>
        );
      default:
        return null;
    }
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      className={`group bg-white dark:bg-gray-800 rounded-lg shadow-sm hover:shadow-md transition-all cursor-move ${
        getPriorityColor(task.priority)
      } ${isDragging ? 'rotate-3 opacity-90' : ''}`}
    >
      <div className="p-4">
        {/* Header */}
        <div className="flex items-start justify-between mb-2">
          <Link
            to={`/tasks/${task.id}`}
            className="flex-1 min-w-0"
            onClick={(e) => e.stopPropagation()}
          >
            <h4 className="font-medium text-sm line-clamp-2 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
              {task.title}
            </h4>
          </Link>
          <DropdownMenu>
            <DropdownMenuTrigger asChild onClick={(e) => e.stopPropagation()}>
              <Button
                variant="ghost"
                size="sm"
                className="h-8 w-8 p-0 opacity-0 group-hover:opacity-100 transition-opacity"
              >
                <MoreVertical className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem asChild>
                <Link to={`/tasks/${task.id}`} className="cursor-pointer">
                  <Eye className="ml-2 h-4 w-4" />
                  مشاهده
                </Link>
              </DropdownMenuItem>
              {onEdit && (
                <DropdownMenuItem onClick={onEdit}>
                  <Edit className="ml-2 h-4 w-4" />
                  ویرایش
                </DropdownMenuItem>
              )}
              <DropdownMenuSeparator />
              {onDelete && (
                <DropdownMenuItem
                  onClick={onDelete}
                  className="text-red-600 dark:text-red-400"
                >
                  <Trash2 className="ml-2 h-4 w-4" />
                  حذف
                </DropdownMenuItem>
              )}
            </DropdownMenuContent>
          </DropdownMenu>
        </div>

        {/* Description */}
        {task.description && (
          <p className="text-xs text-gray-600 dark:text-gray-400 line-clamp-2 mb-3">
            {task.description}
          </p>
        )}

        {/* Tags */}
        {task.tags && (
          <div className="flex flex-wrap gap-1 mb-3">
            {task.tags.split(',').slice(0, 3).map((tag: string, index: number) => (
              <Badge key={index} variant="secondary" className="text-xs">
                {tag.trim()}
              </Badge>
            ))}
          </div>
        )}

        {/* Footer */}
        <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
          <div className="flex items-center gap-2">
            {getPriorityBadge(task.priority)}
            {task.is_overdue && (
              <Badge variant="destructive" className="text-xs">
                <AlertCircle className="ml-1 h-3 w-3" />
                عقب افتاده
              </Badge>
            )}
          </div>
          {task.due_date && (
            <div className="flex items-center gap-1">
              <Calendar className="h-3 w-3" />
              <span>{format(new Date(task.due_date), 'MMM dd', { locale: faIR })}</span>
            </div>
          )}
        </div>

        {/* Created at */}
        <div className="flex items-center gap-1 mt-2 text-xs text-gray-400">
          <Clock className="h-3 w-3" />
          <span>
            {format(new Date(task.created_at), 'PPp', { locale: faIR })}
          </span>
        </div>
      </div>
    </div>
  );
}

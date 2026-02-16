import { useDroppable } from '@dnd-kit/core';
import { SortableContext, verticalListSortingStrategy } from '@dnd-kit/sortable';
import { Badge } from '@/components/ui/badge';
import TaskCard from './TaskCard';

interface KanbanColumnProps {
  id: string;
  title: string;
  tasks: any[];
  color: string;
  onDeleteTask: (id: string) => void;
}

export default function KanbanColumn({
  id,
  title,
  tasks,
  color,
  onDeleteTask,
}: KanbanColumnProps) {
  const { setNodeRef, isOver } = useDroppable({
    id,
  });

  const taskIds = tasks.map((task) => task.id.toString());

  return (
    <div className="flex flex-col h-full">
      {/* Column Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <h3 className="font-semibold text-lg">{title}</h3>
          <Badge variant="secondary" className="rounded-full">
            {tasks.length}
          </Badge>
        </div>
        <div className={`w-3 h-3 rounded-full ${color}`} />
      </div>

      {/* Droppable Area */}
      <SortableContext items={taskIds} strategy={verticalListSortingStrategy}>
        <div
          ref={setNodeRef}
          className={`flex-1 min-h-[500px] p-4 rounded-lg border-2 border-dashed transition-all ${
            isOver
              ? 'border-blue-500 bg-blue-50 dark:bg-blue-950/20'
              : 'border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50'
          }`}
        >
          <div className="space-y-3">
            {tasks.length === 0 ? (
              <div className="text-center py-12 text-gray-400">
                <p className="text-sm">تسکی وجود ندارد</p>
                <p className="text-xs mt-1">تسک را به اینجا بکشید</p>
              </div>
            ) : (
              tasks.map((task) => (
                <TaskCard
                  key={task.id}
                  task={task}
                  onDelete={() => onDeleteTask(task.id.toString())}
                />
              ))
            )}
          </div>
        </div>
      </SortableContext>
    </div>
  );
}

import { useState, useMemo } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  Plus,
  Filter,
  Search,
  SlidersHorizontal,
  Calendar,
  Tag,
  Loader2,
} from 'lucide-react';
import { DndContext, DragEndEvent, DragOverlay, DragStartEvent } from '@dnd-kit/core';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { fetchTasks, updateTask, deleteTask } from '@/services/api';
import TaskCard from '@/components/tasks/TaskCard';
import TaskFormDialog from '@/components/tasks/TaskFormDialog';
import KanbanColumn from '@/components/tasks/KanbanColumn';
import toast from 'react-hot-toast';

const COLUMNS = [
  { id: 'TODO', title: 'برای انجام', color: 'bg-purple-100 dark:bg-purple-900' },
  { id: 'DOING', title: 'در حال انجام', color: 'bg-blue-100 dark:bg-blue-900' },
  { id: 'DONE', title: 'انجام شده', color: 'bg-green-100 dark:bg-green-900' },
];

export default function TasksPage() {
  const queryClient = useQueryClient();
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [priorityFilter, setPriorityFilter] = useState<string>('all');
  const [sortBy, setSortBy] = useState<string>('created_at');
  const [activeId, setActiveId] = useState<string | null>(null);

  // Fetch tasks
  const { data: tasksData, isLoading } = useQuery({
    queryKey: ['tasks', searchQuery, priorityFilter],
    queryFn: () => {
      const params: any = {};
      if (searchQuery) params.search = searchQuery;
      if (priorityFilter !== 'all') params.priority = priorityFilter;
      return fetchTasks(params);
    },
  });

  const tasks = tasksData?.data?.results || [];

  // Update task mutation
  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: any }) => updateTask(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
      toast.success('تسک با موفقیت به‌روزرسانی شد');
    },
    onError: () => {
      toast.error('خطا در به‌روزرسانی تسک');
    },
  });

  // Delete task mutation
  const deleteMutation = useMutation({
    mutationFn: (id: string) => deleteTask(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
      toast.success('تسک با موفقیت حذف شد');
    },
    onError: () => {
      toast.error('خطا در حذف تسک');
    },
  });

  // Group tasks by status
  const tasksByStatus = useMemo(() => {
    const grouped: Record<string, any[]> = {
      TODO: [],
      DOING: [],
      DONE: [],
    };

    tasks.forEach((task: any) => {
      if (grouped[task.status]) {
        grouped[task.status].push(task);
      }
    });

    // Sort tasks
    Object.keys(grouped).forEach((status) => {
      grouped[status].sort((a: any, b: any) => {
        switch (sortBy) {
          case 'priority':
            const priorityOrder = { HIGH: 0, MEDIUM: 1, LOW: 2 };
            return priorityOrder[a.priority as keyof typeof priorityOrder] - 
                   priorityOrder[b.priority as keyof typeof priorityOrder];
          case 'due_date':
            if (!a.due_date) return 1;
            if (!b.due_date) return -1;
            return new Date(a.due_date).getTime() - new Date(b.due_date).getTime();
          case 'created_at':
          default:
            return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
        }
      });
    });

    return grouped;
  }, [tasks, sortBy]);

  // Handle drag start
  const handleDragStart = (event: DragStartEvent) => {
    setActiveId(event.active.id as string);
  };

  // Handle drag end
  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;
    setActiveId(null);

    if (!over) return;

    const taskId = active.id as string;
    const newStatus = over.id as string;

    // Find the task
    const task = tasks.find((t: any) => t.id.toString() === taskId);
    if (!task || task.status === newStatus) return;

    // Update task status
    updateMutation.mutate({
      id: taskId,
      data: { status: newStatus },
    });
  };

  // Handle task delete
  const handleDeleteTask = (id: string) => {
    if (confirm('آیا مطمئن هستید که می‌خواهید این تسک را حذف کنید؟')) {
      deleteMutation.mutate(id);
    }
  };

  // Get active task for drag overlay
  const activeTask = activeId ? tasks.find((t: any) => t.id.toString() === activeId) : null;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">مدیریت تسک‌ها</h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            تسک‌های خود را سازماندهی و پیگیری کنید
          </p>
        </div>
        <Button
          size="lg"
          onClick={() => setIsCreateDialogOpen(true)}
          className="w-full sm:w-auto"
        >
          <Plus className="h-4 w-4 mr-2" />
          تسک جدید
        </Button>
      </div>

      {/* Filters and Search */}
      <div className="flex flex-col lg:flex-row gap-4">
        {/* Search */}
        <div className="relative flex-1">
          <Search className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
          <Input
            type="text"
            placeholder="جستجو در تسک‌ها..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pr-10"
          />
        </div>

        {/* Priority Filter */}
        <Select value={priorityFilter} onValueChange={setPriorityFilter}>
          <SelectTrigger className="w-full lg:w-[180px]">
            <Filter className="h-4 w-4 ml-2" />
            <SelectValue placeholder="اولویت" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">همه اولویت‌ها</SelectItem>
            <SelectItem value="HIGH">بالا</SelectItem>
            <SelectItem value="MEDIUM">متوسط</SelectItem>
            <SelectItem value="LOW">پایین</SelectItem>
          </SelectContent>
        </Select>

        {/* Sort */}
        <Select value={sortBy} onValueChange={setSortBy}>
          <SelectTrigger className="w-full lg:w-[200px]">
            <SlidersHorizontal className="h-4 w-4 ml-2" />
            <SelectValue placeholder="مرتب‌سازی" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="created_at">تاریخ ایجاد</SelectItem>
            <SelectItem value="priority">اولویت</SelectItem>
            <SelectItem value="due_date">تاریخ سررسید</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Stats */}
      <div className="flex items-center gap-4 text-sm">
        <Badge variant="outline" className="px-3 py-1">
          کل: {tasks.length}
        </Badge>
        <Badge variant="outline" className="px-3 py-1 bg-purple-50 text-purple-700">
          برای انجام: {tasksByStatus.TODO.length}
        </Badge>
        <Badge variant="outline" className="px-3 py-1 bg-blue-50 text-blue-700">
          در حال انجام: {tasksByStatus.DOING.length}
        </Badge>
        <Badge variant="outline" className="px-3 py-1 bg-green-50 text-green-700">
          انجام شده: {tasksByStatus.DONE.length}
        </Badge>
      </div>

      {/* Kanban Board */}
      {isLoading ? (
        <div className="flex justify-center items-center py-20">
          <Loader2 className="h-8 w-8 animate-spin text-gray-400" />
        </div>
      ) : (
        <DndContext onDragStart={handleDragStart} onDragEnd={handleDragEnd}>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {COLUMNS.map((column) => (
              <KanbanColumn
                key={column.id}
                id={column.id}
                title={column.title}
                tasks={tasksByStatus[column.id] || []}
                color={column.color}
                onDeleteTask={handleDeleteTask}
              />
            ))}
          </div>

          {/* Drag Overlay */}
          <DragOverlay>
            {activeTask ? (
              <div className="rotate-3 opacity-90">
                <TaskCard task={activeTask} isDragging />
              </div>
            ) : null}
          </DragOverlay>
        </DndContext>
      )}

      {/* Empty State */}
      {!isLoading && tasks.length === 0 && (
        <div className="text-center py-20">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gray-100 dark:bg-gray-800 mb-4">
            <Calendar className="h-8 w-8 text-gray-400" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">
            هیچ تسکی یافت نشد
          </h3>
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            {searchQuery || priorityFilter !== 'all'
              ? 'فیلترهای خود را تغییر دهید یا یک تسک جدید ایجاد کنید'
              : 'برای شروع اولین تسک خود را ایجاد کنید'}
          </p>
          <Button onClick={() => setIsCreateDialogOpen(true)}>
            <Plus className="h-4 w-4 mr-2" />
            ایجاد تسک
          </Button>
        </div>
      )}

      {/* Create Task Dialog */}
      <TaskFormDialog
        open={isCreateDialogOpen}
        onOpenChange={setIsCreateDialogOpen}
        onSuccess={() => {
          queryClient.invalidateQueries({ queryKey: ['tasks'] });
        }}
      />
    </div>
  );
}

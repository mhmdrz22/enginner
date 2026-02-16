import { useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  ArrowLeft,
  Calendar,
  Clock,
  Edit,
  Trash2,
  History,
  Tag,
  User,
  CheckCircle2,
  AlertCircle,
  Loader2,
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { fetchTask, deleteTask, fetchTaskHistory } from '@/services/api';
import TaskFormDialog from '@/components/tasks/TaskFormDialog';
import toast from 'react-hot-toast';
import { format } from 'date-fns';
import { faIR } from 'date-fns/locale';

export default function TaskDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);

  // Fetch task
  const { data: taskData, isLoading } = useQuery({
    queryKey: ['task', id],
    queryFn: () => fetchTask(id!),
    enabled: !!id,
  });

  // Fetch task history
  const { data: historyData } = useQuery({
    queryKey: ['task-history', id],
    queryFn: () => fetchTaskHistory(id!),
    enabled: !!id,
  });

  const task = taskData?.data;
  const history = historyData?.data || [];

  // Delete mutation
  const deleteMutation = useMutation({
    mutationFn: () => deleteTask(id!),
    onSuccess: () => {
      toast.success('تسک با موفقیت حذف شد');
      navigate('/tasks');
    },
    onError: () => {
      toast.error('خطا در حذف تسک');
    },
  });

  const handleDelete = () => {
    if (window.confirm('آیا مطمئن هستید که می‌خواهید این تسک را حذف کنید؟')) {
      deleteMutation.mutate();
    }
  };

  const getPriorityBadge = (priority: string) => {
    switch (priority) {
      case 'HIGH':
        return (
          <Badge className="bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200">
            بالا
          </Badge>
        );
      case 'MEDIUM':
        return (
          <Badge className="bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200">
            متوسط
          </Badge>
        );
      case 'LOW':
        return (
          <Badge className="bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">
            پایین
          </Badge>
        );
      default:
        return <Badge>{priority}</Badge>;
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'TODO':
        return <Badge variant="outline" className="bg-purple-50 text-purple-700">برای انجام</Badge>;
      case 'DOING':
        return <Badge variant="outline" className="bg-blue-50 text-blue-700">در حال انجام</Badge>;
      case 'DONE':
        return <Badge variant="outline" className="bg-green-50 text-green-700">انجام شده</Badge>;
      default:
        return <Badge>{status}</Badge>;
    }
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <Loader2 className="h-8 w-8 animate-spin text-gray-400" />
      </div>
    );
  }

  if (!task) {
    return (
      <div className="text-center py-12">
        <AlertCircle className="mx-auto h-12 w-12 text-gray-400 mb-4" />
        <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">
          تسک یافت نشد
        </h3>
        <Link to="/tasks">
          <Button variant="outline" className="mt-4">
            <ArrowLeft className="ml-2 h-4 w-4" />
            بازگشت به لیست
          </Button>
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <Link to="/tasks">
          <Button variant="ghost" size="sm">
            <ArrowLeft className="ml-2 h-4 w-4" />
            بازگشت
          </Button>
        </Link>
        <div className="flex gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setIsEditDialogOpen(true)}
          >
            <Edit className="ml-2 h-4 w-4" />
            ویرایش
          </Button>
          <Button
            variant="destructive"
            size="sm"
            onClick={handleDelete}
            disabled={deleteMutation.isPending}
          >
            <Trash2 className="ml-2 h-4 w-4" />
            حذف
          </Button>
        </div>
      </div>

      {/* Main Content */}
      <Card>
        <CardHeader>
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-2">
                <CardTitle className="text-3xl">{task.title}</CardTitle>
                {task.is_overdue && (
                  <Badge variant="destructive">عقب افتاده</Badge>
                )}
              </div>
              <div className="flex flex-wrap gap-2 mt-3">
                {getStatusBadge(task.status)}
                {getPriorityBadge(task.priority)}
              </div>
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Description */}
          {task.description && (
            <div>
              <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
                توضیحات
              </h3>
              <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
                {task.description}
              </p>
            </div>
          )}

          <Separator />

          {/* Details Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Created At */}
            <div className="flex items-center gap-3 p-3 rounded-lg border">
              <Clock className="h-5 w-5 text-gray-500" />
              <div>
                <p className="text-sm font-medium">تاریخ ایجاد</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {format(new Date(task.created_at), 'PPP', { locale: faIR })}
                </p>
              </div>
            </div>

            {/* Due Date */}
            {task.due_date && (
              <div className="flex items-center gap-3 p-3 rounded-lg border">
                <Calendar className="h-5 w-5 text-gray-500" />
                <div>
                  <p className="text-sm font-medium">تاریخ سررسید</p>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    {format(new Date(task.due_date), 'PPP', { locale: faIR })}
                  </p>
                </div>
              </div>
            )}

            {/* Completed At */}
            {task.completed_at && (
              <div className="flex items-center gap-3 p-3 rounded-lg border">
                <CheckCircle2 className="h-5 w-5 text-green-500" />
                <div>
                  <p className="text-sm font-medium">تاریخ اتمام</p>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    {format(new Date(task.completed_at), 'PPP', { locale: faIR })}
                  </p>
                </div>
              </div>
            )}

            {/* Tags */}
            {task.tags && (
              <div className="flex items-center gap-3 p-3 rounded-lg border">
                <Tag className="h-5 w-5 text-gray-500" />
                <div>
                  <p className="text-sm font-medium">برچسب‌ها</p>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {task.tags.split(',').map((tag: string, index: number) => (
                      <Badge key={index} variant="secondary" className="text-xs">
                        {tag.trim()}
                      </Badge>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Tabs */}
      <Tabs defaultValue="history" className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="history">
            <History className="ml-2 h-4 w-4" />
            تاریخچه
          </TabsTrigger>
          <TabsTrigger value="activity">
            <User className="ml-2 h-4 w-4" />
            فعالیت‌ها
          </TabsTrigger>
        </TabsList>

        {/* History Tab */}
        <TabsContent value="history">
          <Card>
            <CardHeader>
              <CardTitle>تاریخچه تغییرات</CardTitle>
              <CardDescription>
                تمام تغییرات اعمال شده روی این تسک
              </CardDescription>
            </CardHeader>
            <CardContent>
              {history.length === 0 ? (
                <div className="text-center py-8 text-gray-500">
                  هیچ تغییری ثبت نشده است
                </div>
              ) : (
                <div className="space-y-4">
                  {history.map((record: any, index: number) => (
                    <div
                      key={index}
                      className="flex gap-4 p-4 rounded-lg border border-gray-200 dark:border-gray-700"
                    >
                      <div className="flex-shrink-0">
                        <div className="w-2 h-2 mt-2 rounded-full bg-blue-500" />
                      </div>
                      <div className="flex-1">
                        <p className="text-sm font-medium">{record.change_message}</p>
                        <p className="text-xs text-gray-500 mt-1">
                          {format(new Date(record.changed_at), 'PPpp', { locale: faIR })}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Activity Tab */}
        <TabsContent value="activity">
          <Card>
            <CardHeader>
              <CardTitle>فعالیت‌ها</CardTitle>
              <CardDescription>آخرین فعالیت‌ها روی این تسک</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-8 text-gray-500">
                به زودی اضافه خواهد شد
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Edit Dialog */}
      <TaskFormDialog
        open={isEditDialogOpen}
        onOpenChange={setIsEditDialogOpen}
        task={task}
        onSuccess={() => {
          queryClient.invalidateQueries({ queryKey: ['task', id] });
          queryClient.invalidateQueries({ queryKey: ['tasks'] });
        }}
      />
    </div>
  );
}

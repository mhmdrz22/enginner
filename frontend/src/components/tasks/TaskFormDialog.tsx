import { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useMutation } from '@tanstack/react-query';
import { CalendarIcon, Loader2 } from 'lucide-react';
import { format } from 'date-fns';
import { faIR } from 'date-fns/locale';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Calendar } from '@/components/ui/calendar';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover';
import { createTask, updateTask } from '@/services/api';
import toast from 'react-hot-toast';
import { cn } from '@/lib/utils';

const taskSchema = z.object({
  title: z.string().min(3, 'عنوان حداقل ۳ کاراکتر باشد'),
  description: z.string().optional(),
  status: z.enum(['TODO', 'DOING', 'DONE']),
  priority: z.enum(['LOW', 'MEDIUM', 'HIGH']),
  due_date: z.date().optional().nullable(),
  tags: z.string().optional(),
});

type TaskFormData = z.infer<typeof taskSchema>;

interface TaskFormDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  task?: any;
  onSuccess?: () => void;
}

export default function TaskFormDialog({
  open,
  onOpenChange,
  task,
  onSuccess,
}: TaskFormDialogProps) {
  const isEditMode = !!task;

  const {
    register,
    handleSubmit,
    setValue,
    watch,
    reset,
    formState: { errors },
  } = useForm<TaskFormData>({
    resolver: zodResolver(taskSchema),
    defaultValues: {
      title: '',
      description: '',
      status: 'TODO',
      priority: 'MEDIUM',
      due_date: null,
      tags: '',
    },
  });

  const dueDate = watch('due_date');
  const status = watch('status');
  const priority = watch('priority');

  // Load task data when editing
  useEffect(() => {
    if (task) {
      setValue('title', task.title);
      setValue('description', task.description || '');
      setValue('status', task.status);
      setValue('priority', task.priority);
      setValue('due_date', task.due_date ? new Date(task.due_date) : null);
      setValue('tags', task.tags || '');
    } else {
      reset();
    }
  }, [task, setValue, reset]);

  // Create/Update mutation
  const mutation = useMutation({
    mutationFn: async (data: TaskFormData) => {
      const payload = {
        ...data,
        due_date: data.due_date ? format(data.due_date, 'yyyy-MM-dd') : null,
      };

      if (isEditMode) {
        return updateTask(task.id, payload);
      } else {
        return createTask(payload);
      }
    },
    onSuccess: () => {
      toast.success(
        isEditMode
          ? 'تسک با موفقیت به‌روزرسانی شد'
          : 'تسک با موفقیت ایجاد شد'
      );
      onSuccess?.();
      onOpenChange(false);
      reset();
    },
    onError: (error: any) => {
      console.error('Task mutation error:', error);
      toast.error('خطا در ذخیره تسک. لطفا دوباره تلاش کنید');
    },
  });

  const onSubmit = (data: TaskFormData) => {
    mutation.mutate(data);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[550px] max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>
            {isEditMode ? 'ویرایش تسک' : 'تسک جدید'}
          </DialogTitle>
          <DialogDescription>
            {isEditMode
              ? 'اطلاعات تسک را ویرایش کنید'
              : 'جزئیات تسک جدید را وارد کنید'}
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 mt-4">
          {/* Title */}
          <div className="space-y-2">
            <Label htmlFor="title">عنوان <span className="text-red-500">*</span></Label>
            <Input
              id="title"
              placeholder="عنوان تسک را وارد کنید"
              {...register('title')}
            />
            {errors.title && (
              <p className="text-sm text-red-500">{errors.title.message}</p>
            )}
          </div>

          {/* Description */}
          <div className="space-y-2">
            <Label htmlFor="description">توضیحات</Label>
            <Textarea
              id="description"
              placeholder="توضیحات تسک..."
              rows={4}
              {...register('description')}
            />
          </div>

          {/* Status and Priority */}
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>وضعیت</Label>
              <Select
                value={status}
                onValueChange={(value) => setValue('status', value as any)}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="TODO">برای انجام</SelectItem>
                  <SelectItem value="DOING">در حال انجام</SelectItem>
                  <SelectItem value="DONE">انجام شده</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label>اولویت</Label>
              <Select
                value={priority}
                onValueChange={(value) => setValue('priority', value as any)}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="LOW">پایین</SelectItem>
                  <SelectItem value="MEDIUM">متوسط</SelectItem>
                  <SelectItem value="HIGH">بالا</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          {/* Due Date */}
          <div className="space-y-2">
            <Label>تاریخ سررسید</Label>
            <Popover>
              <PopoverTrigger asChild>
                <Button
                  variant="outline"
                  className={cn(
                    'w-full justify-start text-left font-normal',
                    !dueDate && 'text-muted-foreground'
                  )}
                >
                  <CalendarIcon className="ml-2 h-4 w-4" />
                  {dueDate ? (
                    format(dueDate, 'PPP', { locale: faIR })
                  ) : (
                    <span>تاریخ را انتخاب کنید</span>
                  )}
                </Button>
              </PopoverTrigger>
              <PopoverContent className="w-auto p-0" align="start">
                <Calendar
                  mode="single"
                  selected={dueDate || undefined}
                  onSelect={(date) => setValue('due_date', date || null)}
                  initialFocus
                />
              </PopoverContent>
            </Popover>
          </div>

          {/* Tags */}
          <div className="space-y-2">
            <Label htmlFor="tags">برچسب‌ها</Label>
            <Input
              id="tags"
              placeholder="برچسب‌ها را با کاما جدا کنید (مثل: فوری, مهم)"
              {...register('tags')}
            />
          </div>

          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              onClick={() => onOpenChange(false)}
              disabled={mutation.isPending}
            >
              انصراف
            </Button>
            <Button type="submit" disabled={mutation.isPending}>
              {mutation.isPending ? (
                <>
                  <Loader2 className="ml-2 h-4 w-4 animate-spin" />
                  در حال ذخیره...
                </>
              ) : isEditMode ? (
                'به‌روزرسانی'
              ) : (
                'ایجاد تسک'
              )}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}

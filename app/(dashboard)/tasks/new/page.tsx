'use client';

import * as React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useRouter } from 'next/navigation';
import { ArrowLeft, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
  FormDescription,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { useToast } from '@/hooks/use-toast';

const taskSchema = z.object({
  title: z.string().min(3, 'عنوان باید حداقل 3 کاراکتر باشد'),
  description: z.string().min(10, 'توضیحات باید حداقل 10 کاراکتر باشد'),
  status: z.enum(['pending', 'in_progress', 'completed']),
  priority: z.enum(['low', 'medium', 'high']),
  dueDate: z.string(),
  assigneeId: z.string().optional(),
});

type TaskFormValues = z.infer<typeof taskSchema>;

export default function TaskCreatePage() {
  const router = useRouter();
  const { toast } = useToast();

  const [isLoading, setIsLoading] = React.useState(false);
  const [users, setUsers] = React.useState<Array<{ id: string; name: string }>>([]);

  const form = useForm<TaskFormValues>({
    resolver: zodResolver(taskSchema),
    defaultValues: {
      title: '',
      description: '',
      status: 'pending',
      priority: 'medium',
      dueDate: '',
      assigneeId: '',
    },
  });

  React.useEffect(() => {
    fetchUsers();
  }, []);

  async function fetchUsers() {
    try {
      const response = await fetch('/api/users');
      const data = await response.json();
      setUsers(data.users);
    } catch (error) {
      console.error('Failed to fetch users:', error);
    }
  }

  async function onSubmit(data: TaskFormValues) {
    setIsLoading(true);
    try {
      const response = await fetch('/api/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      if (!response.ok) throw new Error('Failed to create task');

      toast({
        title: 'وظیفه ایجاد شد',
        description: 'وظیفه با موفقیت ایجاد شد',
      });

      router.push('/tasks');
    } catch (error) {
      toast({
        title: 'خطا در ایجاد وظیفه',
        description: 'لطفاً دوباره تلاش کنید',
        variant: 'destructive',
      });
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="space-y-6 p-8">
      <Button
        variant="ghost"
        onClick={() => router.back()}
        className="mb-4"
      >
        <ArrowLeft className="ml-2 h-4 w-4" />
        بازگشت
      </Button>

      <div>
        <h1 className="text-3xl font-bold tracking-tight">ایجاد وظیفه جدید</h1>
        <p className="text-gray-500 dark:text-gray-400">
          یک وظیفه جدید برای تیم خود ایجاد کنید
        </p>
      </div>

      <div className="mx-auto max-w-2xl rounded-lg bg-white p-8 shadow dark:bg-gray-950">
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
            <FormField
              control={form.control}
              name="title"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>عنوان</FormLabel>
                  <FormControl>
                    <Input placeholder="عنوان وظیفه را وارد کنید" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="description"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>توضیحات</FormLabel>
                  <FormControl>
                    <Textarea
                      placeholder="توضیحات کامل وظیفه..."
                      rows={5}
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <div className="grid gap-4 md:grid-cols-2">
              <FormField
                control={form.control}
                name="status"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>وضعیت</FormLabel>
                    <Select onValueChange={field.onChange} value={field.value}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="وضعیت را انتخاب کنید" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="pending">در انتظار</SelectItem>
                        <SelectItem value="in_progress">در حال انجام</SelectItem>
                        <SelectItem value="completed">تکمیل شده</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="priority"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>اولویت</FormLabel>
                    <Select onValueChange={field.onChange} value={field.value}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="اولویت را انتخاب کنید" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="low">کم</SelectItem>
                        <SelectItem value="medium">متوسط</SelectItem>
                        <SelectItem value="high">مهم</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>

            <div className="grid gap-4 md:grid-cols-2">
              <FormField
                control={form.control}
                name="dueDate"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>مهلت انجام</FormLabel>
                    <FormControl>
                      <Input type="date" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="assigneeId"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>مسئول</FormLabel>
                    <Select onValueChange={field.onChange} value={field.value}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="انتخاب مسئول" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        {users.map((user) => (
                          <SelectItem key={user.id} value={user.id}>
                            {user.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <FormDescription>
                      اختیاری - می‌توانید بعداً تخصیص دهید
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>

            <div className="flex gap-4">
              <Button type="submit" disabled={isLoading}>
                {isLoading ? (
                  <>
                    <Loader2 className="ml-2 h-4 w-4 animate-spin" />
                    در حال ذخیره...
                  </>
                ) : (
                  'ایجاد وظیفه'
                )}
              </Button>
              <Button
                type="button"
                variant="outline"
                onClick={() => router.back()}
              >
                انصراف
              </Button>
            </div>
          </form>
        </Form>
      </div>
    </div>
  );
}

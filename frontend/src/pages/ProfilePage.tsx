import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import {
  User,
  Mail,
  Calendar,
  Shield,
  Save,
  Loader2,
  Camera,
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { useAuthStore } from '@/store/authStore';
import { updateProfile } from '@/services/api';
import toast from 'react-hot-toast';
import { format } from 'date-fns';
import { faIR } from 'date-fns/locale';

const profileSchema = z.object({
  first_name: z.string().min(2, 'نام حداقل ۲ کاراکتر باشد'),
  last_name: z.string().min(2, 'نام خانوادگی حداقل ۲ کاراکتر باشد'),
  email: z.string().email('ایمیل معتبر وارد کنید'),
});

type ProfileFormData = z.infer<typeof profileSchema>;

export default function ProfilePage() {
  const queryClient = useQueryClient();
  const user = useAuthStore((state) => state.user);
  const setUser = useAuthStore((state) => state.setUser);
  const [isEditing, setIsEditing] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ProfileFormData>({
    resolver: zodResolver(profileSchema),
    defaultValues: {
      first_name: user?.first_name || '',
      last_name: user?.last_name || '',
      email: user?.email || '',
    },
  });

  const updateMutation = useMutation({
    mutationFn: (data: ProfileFormData) => updateProfile(data),
    onSuccess: (response) => {
      setUser(response.data);
      localStorage.setItem('user', JSON.stringify(response.data));
      setIsEditing(false);
      toast.success('پروفایل با موفقیت به‌روزرسانی شد');
    },
    onError: () => {
      toast.error('خطا در به‌روزرسانی پروفایل');
    },
  });

  const onSubmit = (data: ProfileFormData) => {
    updateMutation.mutate(data);
  };

  const getInitials = () => {
    if (user?.first_name && user?.last_name) {
      return `${user.first_name[0]}${user.last_name[0]}`.toUpperCase();
    }
    return user?.email?.[0].toUpperCase() || 'U';
  };

  const getRoleBadge = () => {
    if (user?.is_superuser) {
      return <Badge className="bg-red-500">مدیر ارشد</Badge>;
    } else if (user?.is_staff) {
      return <Badge className="bg-blue-500">مدیر</Badge>;
    } else {
      return <Badge variant="secondary">کاربر</Badge>;
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight">پروفایل کاربری</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">
          مدیریت اطلاعات حساب کاربری خود
        </p>
      </div>

      {/* Profile Card */}
      <Card>
        <CardHeader>
          <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4">
            {/* Avatar */}
            <div className="relative">
              <Avatar className="h-24 w-24">
                <AvatarImage src={user?.avatar} />
                <AvatarFallback className="text-2xl">{getInitials()}</AvatarFallback>
              </Avatar>
              <button
                className="absolute bottom-0 right-0 p-2 bg-blue-500 text-white rounded-full hover:bg-blue-600 transition-colors"
                title="آپلود تصویر"
              >
                <Camera className="h-4 w-4" />
              </button>
            </div>

            {/* User Info */}
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-2">
                <h2 className="text-2xl font-bold">
                  {user?.first_name && user?.last_name
                    ? `${user.first_name} ${user.last_name}`
                    : user?.email}
                </h2>
                {getRoleBadge()}
              </div>
              <div className="flex flex-wrap gap-4 text-sm text-gray-600 dark:text-gray-400">
                <div className="flex items-center gap-1">
                  <Mail className="h-4 w-4" />
                  {user?.email}
                </div>
                <div className="flex items-center gap-1">
                  <Calendar className="h-4 w-4" />
                  عضو از{' '}
                  {user?.created_date &&
                    format(new Date(user.created_date), 'PPP', { locale: faIR })}
                </div>
              </div>
            </div>

            {/* Edit Button */}
            {!isEditing && (
              <Button onClick={() => setIsEditing(true)} variant="outline">
                ویرایش پروفایل
              </Button>
            )}
          </div>
        </CardHeader>
      </Card>

      {/* Edit Form */}
      {isEditing && (
        <Card>
          <CardHeader>
            <CardTitle>ویرایش اطلاعات</CardTitle>
            <CardDescription>
              اطلاعات حساب کاربری خود را به‌روزرسانی کنید
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              {/* Email (Read-only) */}
              <div className="space-y-2">
                <Label htmlFor="email">ایمیل</Label>
                <Input
                  id="email"
                  type="email"
                  {...register('email')}
                  disabled
                  className="bg-gray-50 dark:bg-gray-900"
                />
                <p className="text-xs text-gray-500">
                  ایمیل قابل تغییر نیست
                </p>
              </div>

              {/* First Name & Last Name */}
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="first_name">نام</Label>
                  <Input
                    id="first_name"
                    type="text"
                    placeholder="نام خود را وارد کنید"
                    {...register('first_name')}
                  />
                  {errors.first_name && (
                    <p className="text-sm text-red-500">{errors.first_name.message}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="last_name">نام خانوادگی</Label>
                  <Input
                    id="last_name"
                    type="text"
                    placeholder="نام خانوادگی خود را وارد کنید"
                    {...register('last_name')}
                  />
                  {errors.last_name && (
                    <p className="text-sm text-red-500">{errors.last_name.message}</p>
                  )}
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex gap-2 pt-4">
                <Button
                  type="submit"
                  disabled={updateMutation.isPending}
                  className="flex-1"
                >
                  {updateMutation.isPending ? (
                    <>
                      <Loader2 className="ml-2 h-4 w-4 animate-spin" />
                      در حال ذخیره...
                    </>
                  ) : (
                    <>
                      <Save className="ml-2 h-4 w-4" />
                      ذخیره تغییرات
                    </>
                  )}
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setIsEditing(false)}
                  disabled={updateMutation.isPending}
                >
                  انصراف
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}

      {/* Account Details */}
      <Card>
        <CardHeader>
          <CardTitle>جزئیات حساب</CardTitle>
          <CardDescription>اطلاعات حساب کاربری شما</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Account Status */}
            <div className="flex items-center justify-between p-4 rounded-lg border">
              <div className="flex items-center gap-3">
                <Shield className="h-5 w-5 text-gray-500" />
                <div>
                  <p className="text-sm font-medium">وضعیت حساب</p>
                  <p className="text-xs text-gray-500">فعال یا غیرفعال</p>
                </div>
              </div>
              <Badge variant={user?.is_active ? 'default' : 'destructive'}>
                {user?.is_active ? 'فعال' : 'غیرفعال'}
              </Badge>
            </div>

            {/* Email Verification */}
            <div className="flex items-center justify-between p-4 rounded-lg border">
              <div className="flex items-center gap-3">
                <Mail className="h-5 w-5 text-gray-500" />
                <div>
                  <p className="text-sm font-medium">تایید ایمیل</p>
                  <p className="text-xs text-gray-500">وضعیت تایید ایمیل</p>
                </div>
              </div>
              <Badge variant={user?.is_verified ? 'default' : 'secondary'}>
                {user?.is_verified ? 'تایید شده' : 'تایید نشده'}
              </Badge>
            </div>

            {/* User Role */}
            <div className="flex items-center justify-between p-4 rounded-lg border">
              <div className="flex items-center gap-3">
                <User className="h-5 w-5 text-gray-500" />
                <div>
                  <p className="text-sm font-medium">نقش کاربری</p>
                  <p className="text-xs text-gray-500">سطح دسترسی</p>
                </div>
              </div>
              {getRoleBadge()}
            </div>

            {/* Last Login */}
            <div className="flex items-center justify-between p-4 rounded-lg border">
              <div className="flex items-center gap-3">
                <Calendar className="h-5 w-5 text-gray-500" />
                <div>
                  <p className="text-sm font-medium">آخرین ورود</p>
                  <p className="text-xs text-gray-500">
                    {user?.last_login_date
                      ? format(new Date(user.last_login_date), 'PPP', { locale: faIR })
                      : 'هرگز'}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Danger Zone */}
      <Card className="border-red-200 dark:border-red-900">
        <CardHeader>
          <CardTitle className="text-red-600 dark:text-red-400">
            منطقه خطرناک
          </CardTitle>
          <CardDescription>
            اقدامات غیرقابل برگشت بر روی حساب
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex items-center justify-between p-4 rounded-lg border border-red-200 dark:border-red-900">
            <div>
              <p className="font-medium text-sm">حذف حساب</p>
              <p className="text-xs text-gray-500 mt-1">
                حساب و تمام داده‌های شما به طور کامل حذف خواهد شد
              </p>
            </div>
            <Button variant="destructive" size="sm">
              حذف حساب
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

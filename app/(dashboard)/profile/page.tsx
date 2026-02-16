'use client';

import * as React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Camera, Loader2, Mail, User } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { useToast } from '@/hooks/use-toast';

const profileSchema = z.object({
  name: z.string().min(2, 'نام باید حداقل 2 کاراکتر باشد'),
  email: z.string().email('ایمیل معتبر وارد کنید'),
  bio: z.string().optional(),
});

const passwordSchema = z
  .object({
    currentPassword: z.string().min(6),
    newPassword: z.string().min(8, 'رمز عبور باید حداقل 8 کاراکتر باشد'),
    confirmPassword: z.string(),
  })
  .refine((data) => data.newPassword === data.confirmPassword, {
    message: 'رمز عبور و تکرار آن مطابقت ندارند',
    path: ['confirmPassword'],
  });

type ProfileFormValues = z.infer<typeof profileSchema>;
type PasswordFormValues = z.infer<typeof passwordSchema>;

export default function ProfilePage() {
  const { toast } = useToast();
  const [isLoading, setIsLoading] = React.useState(false);
  const [user, setUser] = React.useState({
    name: 'کاربر تستی',
    email: 'user@example.com',
    avatar: '',
    bio: '',
  });

  const profileForm = useForm<ProfileFormValues>({
    resolver: zodResolver(profileSchema),
    defaultValues: user,
  });

  const passwordForm = useForm<PasswordFormValues>({
    resolver: zodResolver(passwordSchema),
  });

  async function onProfileSubmit(data: ProfileFormValues) {
    setIsLoading(true);
    try {
      const response = await fetch('/api/user/profile', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      if (!response.ok) throw new Error('Update failed');

      toast({
        title: 'پروفایل به‌روزرسانی شد',
        description: 'اطلاعات شما با موفقیت ذخیره شد',
      });

      setUser({ ...user, ...data });
    } catch (error) {
      toast({
        title: 'خطا در به‌روزرسانی',
        variant: 'destructive',
      });
    } finally {
      setIsLoading(false);
    }
  }

  async function onPasswordSubmit(data: PasswordFormValues) {
    setIsLoading(true);
    try {
      const response = await fetch('/api/user/password', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      if (!response.ok) throw new Error('Update failed');

      toast({
        title: 'رمز عبور تغییر کرد',
        description: 'رمز عبور شما با موفقیت به‌روزرسانی شد',
      });

      passwordForm.reset();
    } catch (error) {
      toast({
        title: 'خطا در تغییر رمز عبور',
        variant: 'destructive',
      });
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="space-y-6 p-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">پروفایل کاربری</h1>
        <p className="text-gray-500 dark:text-gray-400">
          مدیریت اطلاعات حساب کاربری خود
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        {/* Avatar Card */}
        <Card>
          <CardHeader>
            <CardTitle>تصویر پروفایل</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col items-center space-y-4">
            <Avatar className="h-32 w-32">
              <AvatarImage src={user.avatar} />
              <AvatarFallback className="text-2xl">
                {user.name.charAt(0)}
              </AvatarFallback>
            </Avatar>
            <Button variant="outline" size="sm">
              <Camera className="ml-2 h-4 w-4" />
              تغییر تصویر
            </Button>
          </CardContent>
        </Card>

        {/* Forms */}
        <div className="lg:col-span-2">
          <Tabs defaultValue="profile">
            <TabsList>
              <TabsTrigger value="profile">اطلاعات شخصی</TabsTrigger>
              <TabsTrigger value="password">تغییر رمز عبور</TabsTrigger>
            </TabsList>

            <TabsContent value="profile">
              <Card>
                <CardHeader>
                  <CardTitle>اطلاعات شخصی</CardTitle>
                  <CardDescription>
                    اطلاعات پروفایل خود را به‌روزرسانی کنید
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Form {...profileForm}>
                    <form
                      onSubmit={profileForm.handleSubmit(onProfileSubmit)}
                      className="space-y-4"
                    >
                      <FormField
                        control={profileForm.control}
                        name="name"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>نام کامل</FormLabel>
                            <FormControl>
                              <Input {...field} />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />

                      <FormField
                        control={profileForm.control}
                        name="email"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>ایمیل</FormLabel>
                            <FormControl>
                              <Input type="email" {...field} />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />

                      <FormField
                        control={profileForm.control}
                        name="bio"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>بیوگرافی</FormLabel>
                            <FormControl>
                              <Input {...field} placeholder="درباره خود بنویسید" />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />

                      <Button type="submit" disabled={isLoading}>
                        {isLoading ? (
                          <>
                            <Loader2 className="ml-2 h-4 w-4 animate-spin" />
                            در حال ذخیره...
                          </>
                        ) : (
                          'ذخیره تغییرات'
                        )}
                      </Button>
                    </form>
                  </Form>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="password">
              <Card>
                <CardHeader>
                  <CardTitle>تغییر رمز عبور</CardTitle>
                  <CardDescription>
                    رمز عبور خود را تغییر دهید
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Form {...passwordForm}>
                    <form
                      onSubmit={passwordForm.handleSubmit(onPasswordSubmit)}
                      className="space-y-4"
                    >
                      <FormField
                        control={passwordForm.control}
                        name="currentPassword"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>رمز عبور فعلی</FormLabel>
                            <FormControl>
                              <Input type="password" {...field} />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />

                      <FormField
                        control={passwordForm.control}
                        name="newPassword"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>رمز عبور جدید</FormLabel>
                            <FormControl>
                              <Input type="password" {...field} />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />

                      <FormField
                        control={passwordForm.control}
                        name="confirmPassword"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>تکرار رمز عبور جدید</FormLabel>
                            <FormControl>
                              <Input type="password" {...field} />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />

                      <Button type="submit" disabled={isLoading}>
                        {isLoading ? (
                          <>
                            <Loader2 className="ml-2 h-4 w-4 animate-spin" />
                            در حال ذخیره...
                          </>
                        ) : (
                          'تغییر رمز عبور'
                        )}
                      </Button>
                    </form>
                  </Form>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  );
}

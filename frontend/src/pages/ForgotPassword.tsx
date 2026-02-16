import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Mail, ArrowLeft, CheckCircle2, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import toast from 'react-hot-toast';
import api from '@/services/api';

const forgotPasswordSchema = z.object({
  email: z.string().email('ایمیل معتبر وارد کنید'),
});

type ForgotPasswordFormData = z.infer<typeof forgotPasswordSchema>;

export default function ForgotPassword() {
  const [isLoading, setIsLoading] = useState(false);
  const [emailSent, setEmailSent] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ForgotPasswordFormData>({
    resolver: zodResolver(forgotPasswordSchema),
    defaultValues: {
      email: '',
    },
  });

  const onSubmit = async (data: ForgotPasswordFormData) => {
    setIsLoading(true);
    try {
      await api.post('/accounts/password-reset/', data);
      setEmailSent(true);
      toast.success('لینک بازیابی رمز عبور به ایمیل شما ارسال شد');
    } catch (error: any) {
      console.error('Password reset error:', error);
      if (error.response?.data?.email) {
        toast.error('این ایمیل در سیستم یافت نشد');
      } else {
        toast.error('خطا در ارسال ایمیل. لطفا دوباره تلاش کنید');
      }
    } finally {
      setIsLoading(false);
    }
  };

  if (emailSent) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 p-4">
        <Card className="w-full max-w-md shadow-xl">
          <CardHeader className="text-center">
            <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-green-100 dark:bg-green-900">
              <CheckCircle2 className="h-6 w-6 text-green-600 dark:text-green-400" />
            </div>
            <CardTitle className="text-2xl">ایمیل ارسال شد!</CardTitle>
            <CardDescription className="mt-2">
              لینک بازیابی رمز عبور به ایمیل شما ارسال شد. لطفا صندوق ورودی خود را بررسی کنید.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="rounded-lg border border-blue-200 bg-blue-50 p-4 dark:border-blue-900 dark:bg-blue-950">
              <p className="text-sm text-blue-800 dark:text-blue-200">
                <strong>نکته:</strong> اگر ایمیل را دریافت نکردید، پوشه spam خود را بررسی کنید.
              </p>
            </div>
            <Link to="/login" className="block">
              <Button variant="outline" className="w-full">
                <ArrowLeft className="ml-2 h-4 w-4" />
                بازگشت به صفحه ورود
              </Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 p-4">
      <Card className="w-full max-w-md shadow-xl">
        <CardHeader className="space-y-1 text-center">
          <CardTitle className="text-3xl font-bold">فراموشی رمز عبور</CardTitle>
          <CardDescription>
            ایمیل خود را وارد کنید تا لینک بازیابی برای شما ارسال شود
          </CardDescription>
        </CardHeader>
        
        <CardContent>
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            {/* Email Field */}
            <div className="space-y-2">
              <Label htmlFor="email">ایمیل</Label>
              <div className="relative">
                <Mail className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                <Input
                  id="email"
                  type="email"
                  placeholder="example@email.com"
                  className="pl-10"
                  disabled={isLoading}
                  {...register('email')}
                />
              </div>
              {errors.email && (
                <p className="text-sm text-red-500">{errors.email.message}</p>
              )}
            </div>

            {/* Info Box */}
            <div className="rounded-lg border border-gray-200 bg-gray-50 p-4 dark:border-gray-700 dark:bg-gray-900">
              <p className="text-sm text-gray-600 dark:text-gray-400">
                پس از ارسال، یک ایمیل حاوی لینک بازیابی رمز عبور دریافت خواهید کرد.
              </p>
            </div>

            {/* Submit Button */}
            <Button
              type="submit"
              className="w-full"
              size="lg"
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  در حال ارسال...
                </>
              ) : (
                'ارسال لینک بازیابی'
              )}
            </Button>

            {/* Back to Login */}
            <div className="text-center">
              <Link
                to="/login"
                className="text-sm text-blue-600 hover:text-blue-800 dark:text-blue-400 inline-flex items-center"
              >
                <ArrowLeft className="ml-1 h-4 w-4" />
                بازگشت به صفحه ورود
              </Link>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}

import Link from 'next/link';
import { FileQuestion, Home } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function NotFound() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50 dark:bg-gray-900">
      <div className="mx-auto max-w-md px-4 text-center">
        <div className="mb-8 flex justify-center">
          <div className="rounded-full bg-red-100 p-6 dark:bg-red-900/20">
            <FileQuestion className="h-16 w-16 text-red-600 dark:text-red-400" />
          </div>
        </div>

        <h1 className="mb-2 text-6xl font-bold text-gray-900 dark:text-white">
          404
        </h1>
        <h2 className="mb-4 text-2xl font-semibold text-gray-700 dark:text-gray-300">
          صفحه یافت نشد
        </h2>
        <p className="mb-8 text-gray-600 dark:text-gray-400">
          متأسفانه، صفحه‌ای که دنبال آن می‌گردید پیدا نشد. لطفاً آدرس را بررسی کنید یا به صفحه اصلی بازگردید.
        </p>

        <div className="flex flex-col gap-3 sm:flex-row sm:justify-center">
          <Link href="/dashboard">
            <Button className="w-full sm:w-auto">
              <Home className="ml-2 h-4 w-4" />
              بازگشت به خانه
            </Button>
          </Link>
          <Button
            variant="outline"
            onClick={() => window.history.back()}
            className="w-full sm:w-auto"
          >
            بازگشت به صفحه قبل
          </Button>
        </div>

        <div className="mt-12 text-sm text-gray-500 dark:text-gray-400">
          <p>نیاز به کمک دارید؟</p>
          <Link
            href="/support"
            className="text-blue-600 hover:underline dark:text-blue-400"
          >
            تماس با پشتیبانی
          </Link>
        </div>
      </div>
    </div>
  );
}

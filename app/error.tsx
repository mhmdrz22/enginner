'use client';

import { useEffect } from 'react';
import { AlertTriangle, RefreshCcw, Home } from 'lucide-react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log error to error reporting service
    console.error(error);
  }, [error]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50 dark:bg-gray-900">
      <div className="mx-auto max-w-md px-4 text-center">
        <div className="mb-8 flex justify-center">
          <div className="rounded-full bg-orange-100 p-6 dark:bg-orange-900/20">
            <AlertTriangle className="h-16 w-16 text-orange-600 dark:text-orange-400" />
          </div>
        </div>

        <h1 className="mb-2 text-4xl font-bold text-gray-900 dark:text-white">
          مشکلی پیش آمده!
        </h1>
        <h2 className="mb-4 text-xl font-semibold text-gray-700 dark:text-gray-300">
          خطای غیرمنتظره
        </h2>
        <p className="mb-8 text-gray-600 dark:text-gray-400">
          متأسفانه، در بارگذاری این صفحه مشکلی پیش آمده است. لطفاً دوباره تلاش کنید یا به صفحه اصلی بازگردید.
        </p>

        {error.digest && (
          <div className="mb-6 rounded-lg bg-gray-100 p-4 dark:bg-gray-800">
            <p className="text-sm text-gray-600 dark:text-gray-400">
              کد خطا:{' '}
              <code className="font-mono text-xs">{error.digest}</code>
            </p>
          </div>
        )}

        <div className="flex flex-col gap-3 sm:flex-row sm:justify-center">
          <Button onClick={reset} className="w-full sm:w-auto">
            <RefreshCcw className="ml-2 h-4 w-4" />
            تلاش مجدد
          </Button>
          <Link href="/dashboard">
            <Button variant="outline" className="w-full sm:w-auto">
              <Home className="ml-2 h-4 w-4" />
              بازگشت به خانه
            </Button>
          </Link>
        </div>

        <div className="mt-12 text-sm text-gray-500 dark:text-gray-400">
          <p>اگر مشکل ادامه داشت، لطفاً با پشتیبانی تماس بگیرید.</p>
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

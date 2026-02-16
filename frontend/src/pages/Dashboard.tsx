import { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import {
  LayoutDashboard,
  CheckCircle2,
  Clock,
  AlertCircle,
  TrendingUp,
  Plus,
  ArrowRight,
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { fetchTasks, fetchTaskStatistics } from '@/services/api';
import { useAuthStore } from '@/store/authStore';
import { formatDistanceToNow } from 'date-fns';
import { faIR } from 'date-fns/locale';

interface StatCard {
  title: string;
  value: number | string;
  description: string;
  icon: any;
  color: string;
  bgColor: string;
}

export default function Dashboard() {
  const user = useAuthStore((state) => state.user);

  // Fetch tasks
  const { data: tasksData, isLoading: tasksLoading } = useQuery({
    queryKey: ['tasks'],
    queryFn: () => fetchTasks(),
  });

  // Fetch statistics
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['task-statistics'],
    queryFn: () => fetchTaskStatistics(),
  });

  const tasks = tasksData?.data?.results || [];
  const recentTasks = tasks.slice(0, 5);

  // Calculate stats from local data if API doesn't provide them
  const todoCount = tasks.filter((t: any) => t.status === 'TODO').length;
  const doingCount = tasks.filter((t: any) => t.status === 'DOING').length;
  const doneCount = tasks.filter((t: any) => t.status === 'DONE').length;
  const overdueCount = tasks.filter((t: any) => t.is_overdue).length;

  const statCards: StatCard[] = [
    {
      title: 'تسک‌های انجام شده',
      value: stats?.by_status?.DONE || doneCount,
      description: 'تسک‌های تکمیل شده',
      icon: CheckCircle2,
      color: 'text-green-600',
      bgColor: 'bg-green-50 dark:bg-green-950',
    },
    {
      title: 'در حال انجام',
      value: stats?.by_status?.DOING || doingCount,
      description: 'تسک‌های در حال پیشرفت',
      icon: Clock,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50 dark:bg-blue-950',
    },
    {
      title: 'برای انجام',
      value: stats?.by_status?.TODO || todoCount,
      description: 'تسک‌های جدید',
      icon: LayoutDashboard,
      color: 'text-purple-600',
      bgColor: 'bg-purple-50 dark:bg-purple-950',
    },
    {
      title: 'عقب افتاده',
      value: stats?.overdue || overdueCount,
      description: 'نیاز به توجه فوری',
      icon: AlertCircle,
      color: 'text-red-600',
      bgColor: 'bg-red-50 dark:bg-red-950',
    },
  ];

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'HIGH':
        return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200';
      case 'MEDIUM':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200';
      case 'LOW':
        return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200';
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
        return <Badge variant="outline">{status}</Badge>;
    }
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">
            سلام {user?.first_name || user?.email} 👋
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            اینجا خلاصه‌ای از وضعیت تسک‌های شما است
          </p>
        </div>
        <Link to="/tasks">
          <Button size="lg" className="w-full sm:w-auto">
            <Plus className="h-4 w-4 mr-2" />
            تسک جدید
          </Button>
        </Link>
      </div>

      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {statCards.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <Card key={index} className="hover:shadow-lg transition-shadow">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  {stat.title}
                </CardTitle>
                <div className={`p-2 rounded-lg ${stat.bgColor}`}>
                  <Icon className={`h-4 w-4 ${stat.color}`} />
                </div>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">{stat.value}</div>
                <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                  {stat.description}
                </p>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Progress Overview */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5" />
            پیشرفت کلی
          </CardTitle>
          <CardDescription>
            وضعیت انجام تسک‌ها
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {/* Progress Bar */}
            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-600 dark:text-gray-400">درصد انجام</span>
                <span className="font-medium">
                  {tasks.length > 0
                    ? Math.round((doneCount / tasks.length) * 100)
                    : 0}%
                </span>
              </div>
              <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-green-500 to-emerald-600 rounded-full transition-all duration-500"
                  style={{
                    width: `${tasks.length > 0 ? (doneCount / tasks.length) * 100 : 0}%`,
                  }}
                />
              </div>
            </div>

            {/* Status Distribution */}
            <div className="grid grid-cols-3 gap-4 mt-6">
              <div className="text-center">
                <div className="text-2xl font-bold text-purple-600">{todoCount}</div>
                <div className="text-xs text-gray-600 dark:text-gray-400 mt-1">برای انجام</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">{doingCount}</div>
                <div className="text-xs text-gray-600 dark:text-gray-400 mt-1">در حال انجام</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">{doneCount}</div>
                <div className="text-xs text-gray-600 dark:text-gray-400 mt-1">انجام شده</div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Recent Tasks */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>تسک‌های اخیر</CardTitle>
              <CardDescription>آخرین تسک‌های شما</CardDescription>
            </div>
            <Link to="/tasks">
              <Button variant="ghost" size="sm">
                مشاهده همه
                <ArrowRight className="mr-2 h-4 w-4" />
              </Button>
            </Link>
          </div>
        </CardHeader>
        <CardContent>
          {tasksLoading ? (
            <div className="flex justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900 dark:border-gray-100" />
            </div>
          ) : recentTasks.length === 0 ? (
            <div className="text-center py-12">
              <LayoutDashboard className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-4 text-lg font-medium text-gray-900 dark:text-gray-100">
                تسکی وجود ندارد
              </h3>
              <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
                برای شروع یک تسک جدید ایجاد کنید
              </p>
              <Link to="/tasks">
                <Button className="mt-4">
                  <Plus className="h-4 w-4 mr-2" />
                  اولین تسک
                </Button>
              </Link>
            </div>
          ) : (
            <div className="space-y-3">
              {recentTasks.map((task: any) => (
                <div
                  key={task.id}
                  className="flex items-center justify-between p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                >
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <h4 className="text-sm font-medium truncate">{task.title}</h4>
                      {task.is_overdue && (
                        <Badge variant="destructive" className="text-xs">
                          عقب افتاده
                        </Badge>
                      )}
                    </div>
                    <div className="flex items-center gap-2 mt-1">
                      {getStatusBadge(task.status)}
                      <Badge className={getPriorityColor(task.priority)}>
                        {task.priority === 'HIGH' && 'بالا'}
                        {task.priority === 'MEDIUM' && 'متوسط'}
                        {task.priority === 'LOW' && 'پایین'}
                      </Badge>
                      <span className="text-xs text-gray-500">
                        {formatDistanceToNow(new Date(task.created_at), {
                          addSuffix: true,
                          locale: faIR,
                        })}
                      </span>
                    </div>
                  </div>
                  <Link to={`/tasks/${task.id}`}>
                    <Button variant="ghost" size="sm">
                      <ArrowRight className="h-4 w-4" />
                    </Button>
                  </Link>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

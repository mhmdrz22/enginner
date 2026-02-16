import { useQuery } from '@tanstack/react-query';
import {
  Users,
  CheckSquare,
  Activity,
  TrendingUp,
  AlertCircle,
  UserCheck,
  UserX,
  Shield,
  Clock,
  Calendar,
  BarChart3,
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import LoadingSpinner from '@/components/ui/loading-spinner';
import api from '@/services/api';
import { format } from 'date-fns';
import { faIR } from 'date-fns/locale';
import { useAuthStore } from '@/store/authStore';
import { Navigate } from 'react-router-dom';

export default function AdminDashboard() {
  const user = useAuthStore((state) => state.user);

  // Check if user is admin
  if (!user?.is_staff && !user?.is_superuser) {
    return <Navigate to="/dashboard" replace />;
  }

  // Fetch admin statistics
  const { data: statsData, isLoading: statsLoading } = useQuery({
    queryKey: ['admin-stats'],
    queryFn: async () => {
      const response = await api.get('/admin/statistics/');
      return response.data;
    },
  });

  // Fetch users list
  const { data: usersData, isLoading: usersLoading } = useQuery({
    queryKey: ['admin-users'],
    queryFn: async () => {
      const response = await api.get('/admin/users/');
      return response.data;
    },
  });

  // Fetch recent activities
  const { data: activitiesData, isLoading: activitiesLoading } = useQuery({
    queryKey: ['admin-activities'],
    queryFn: async () => {
      const response = await api.get('/admin/activities/');
      return response.data;
    },
  });

  const stats = statsData || {};
  const users = usersData?.results || [];
  const activities = activitiesData?.results || [];

  if (statsLoading || usersLoading || activitiesLoading) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">پنل مدیریت</h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            مدیریت کاربران و سیستم
          </p>
        </div>
        <Badge className="bg-gradient-to-r from-purple-500 to-pink-500">
          <Shield className="ml-1 h-3 w-3" />
          {user?.is_superuser ? 'مدیر ارشد' : 'مدیر'}
        </Badge>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Total Users */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">کل کاربران</CardTitle>
            <Users className="h-4 w-4 text-gray-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.total_users || 0}</div>
            <p className="text-xs text-gray-500 mt-1">
              <span className="text-green-500">▲ +{stats.new_users_this_month || 0}</span> این ماه
            </p>
          </CardContent>
        </Card>

        {/* Active Users */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">کاربران فعال</CardTitle>
            <UserCheck className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.active_users || 0}</div>
            <p className="text-xs text-gray-500 mt-1">
              {stats.active_users_percentage || 0}% از کل کاربران
            </p>
          </CardContent>
        </Card>

        {/* Total Tasks */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">کل تسک‌ها</CardTitle>
            <CheckSquare className="h-4 w-4 text-blue-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.total_tasks || 0}</div>
            <p className="text-xs text-gray-500 mt-1">
              <span className="text-blue-500">{stats.tasks_created_today || 0}</span> امروز
            </p>
          </CardContent>
        </Card>

        {/* System Activity */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">فعالیت سیستم</CardTitle>
            <Activity className="h-4 w-4 text-purple-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.activities_today || 0}</div>
            <p className="text-xs text-gray-500 mt-1">فعالیت امروز</p>
          </CardContent>
        </Card>
      </div>

      {/* Tabs */}
      <Tabs defaultValue="users" className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="users">
            <Users className="ml-2 h-4 w-4" />
            کاربران
          </TabsTrigger>
          <TabsTrigger value="activities">
            <Activity className="ml-2 h-4 w-4" />
            فعالیت‌ها
          </TabsTrigger>
          <TabsTrigger value="analytics">
            <BarChart3 className="ml-2 h-4 w-4" />
            آمار
          </TabsTrigger>
        </TabsList>

        {/* Users Tab */}
        <TabsContent value="users">
          <Card>
            <CardHeader>
              <CardTitle>لیست کاربران</CardTitle>
              <CardDescription>مدیریت و نظارت بر کاربران</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {users.length === 0 ? (
                  <div className="text-center py-8 text-gray-500">
                    کاربری یافت نشد
                  </div>
                ) : (
                  users.slice(0, 10).map((userItem: any) => (
                    <div
                      key={userItem.id}
                      className="flex items-center justify-between p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                    >
                      <div className="flex items-center gap-3">
                        <div className="h-10 w-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white font-semibold">
                          {userItem.email[0].toUpperCase()}
                        </div>
                        <div>
                          <p className="font-medium">
                            {userItem.first_name && userItem.last_name
                              ? `${userItem.first_name} ${userItem.last_name}`
                              : userItem.email}
                          </p>
                          <p className="text-sm text-gray-500">{userItem.email}</p>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        {userItem.is_superuser && (
                          <Badge className="bg-red-500">مدیر ارشد</Badge>
                        )}
                        {userItem.is_staff && !userItem.is_superuser && (
                          <Badge className="bg-blue-500">مدیر</Badge>
                        )}
                        <Badge variant={userItem.is_active ? 'default' : 'secondary'}>
                          {userItem.is_active ? 'فعال' : 'غیرفعال'}
                        </Badge>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Activities Tab */}
        <TabsContent value="activities">
          <Card>
            <CardHeader>
              <CardTitle>فعالیت‌های اخیر</CardTitle>
              <CardDescription>لاگ فعالیت‌های سیستم</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {activities.length === 0 ? (
                  <div className="text-center py-8 text-gray-500">
                    فعالیتی ثبت نشده است
                  </div>
                ) : (
                  activities.slice(0, 15).map((activity: any, index: number) => (
                    <div
                      key={index}
                      className="flex items-start gap-3 p-3 rounded-lg border border-gray-200 dark:border-gray-700"
                    >
                      <div className="flex-shrink-0 mt-1">
                        <Activity className="h-4 w-4 text-blue-500" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium">{activity.description}</p>
                        <div className="flex items-center gap-2 mt-1 text-xs text-gray-500">
                          <Clock className="h-3 w-3" />
                          {format(new Date(activity.created_at), 'PPp', { locale: faIR })}
                        </div>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Analytics Tab */}
        <TabsContent value="analytics">
          <Card>
            <CardHeader>
              <CardTitle>آمار سیستم</CardTitle>
              <CardDescription>آمار جامع عملکرد سیستم</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Task Statistics */}
                <div className="p-4 rounded-lg border">
                  <h4 className="font-semibold mb-3 flex items-center gap-2">
                    <CheckSquare className="h-4 w-4" />
                    آمار تسک‌ها
                  </h4>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">برای انجام:</span>
                      <span className="font-medium">{stats.tasks_todo || 0}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">در حال انجام:</span>
                      <span className="font-medium">{stats.tasks_doing || 0}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">انجام شده:</span>
                      <span className="font-medium">{stats.tasks_done || 0}</span>
                    </div>
                    <div className="flex justify-between text-sm pt-2 border-t">
                      <span className="text-gray-600">عقب افتاده:</span>
                      <span className="font-medium text-red-500">
                        {stats.tasks_overdue || 0}
                      </span>
                    </div>
                  </div>
                </div>

                {/* User Statistics */}
                <div className="p-4 rounded-lg border">
                  <h4 className="font-semibold mb-3 flex items-center gap-2">
                    <Users className="h-4 w-4" />
                    آمار کاربران
                  </h4>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">فعال:</span>
                      <span className="font-medium text-green-500">
                        {stats.active_users || 0}
                      </span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">غیرفعال:</span>
                      <span className="font-medium text-gray-500">
                        {stats.inactive_users || 0}
                      </span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">مدیران:</span>
                      <span className="font-medium">{stats.staff_users || 0}</span>
                    </div>
                    <div className="flex justify-between text-sm pt-2 border-t">
                      <span className="text-gray-600">عضو این ماه:</span>
                      <span className="font-medium text-blue-500">
                        {stats.new_users_this_month || 0}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Additional Info */}
              <div className="mt-4 p-4 rounded-lg bg-blue-50 dark:bg-blue-950 border border-blue-200 dark:border-blue-900">
                <p className="text-sm text-blue-800 dark:text-blue-200">
                  <strong>کل:</strong> {stats.total_users || 0} کاربر در سیستم ثبت‌نام کرده‌اند و{' '}
                  {stats.total_tasks || 0} تسک ایجاد شده است.
                </p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}

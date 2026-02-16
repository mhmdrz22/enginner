'use client';

import * as React from 'react';
import {
  Users,
  CheckCircle2,
  Clock,
  AlertCircle,
  Activity,
  TrendingUp,
  TrendingDown,
} from 'lucide-react';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';

export default function AdminDashboard() {
  const stats = [
    {
      title: 'کل کاربران',
      value: '1,234',
      change: '+12%',
      trend: 'up',
      icon: Users,
      description: 'نسبت به ماه گذشته',
    },
    {
      title: 'وظایف تکمیل شده',
      value: '856',
      change: '+8%',
      trend: 'up',
      icon: CheckCircle2,
      description: 'در این ماه',
    },
    {
      title: 'وظایف در حال انجام',
      value: '245',
      change: '-3%',
      trend: 'down',
      icon: Clock,
      description: 'نسبت به هفته گذشته',
    },
    {
      title: 'وظایف معوق',
      value: '12',
      change: '-25%',
      trend: 'up',
      icon: AlertCircle,
      description: 'بهبود یافته',
    },
  ];

  const recentUsers = [
    {
      id: '1',
      name: 'علی احمدی',
      email: 'ali@example.com',
      role: 'ادمین',
      status: 'active',
      joinDate: '1403/10/15',
    },
    {
      id: '2',
      name: 'سارا محمدی',
      email: 'sara@example.com',
      role: 'کاربر',
      status: 'active',
      joinDate: '1403/10/14',
    },
    {
      id: '3',
      name: 'رضا کریمی',
      email: 'reza@example.com',
      role: 'کاربر',
      status: 'inactive',
      joinDate: '1403/10/13',
    },
    {
      id: '4',
      name: 'مریم حسینی',
      email: 'maryam@example.com',
      role: 'کاربر',
      status: 'active',
      joinDate: '1403/10/12',
    },
  ];

  const topPerformers = [
    { name: 'علی احمدی', tasks: 45, avatar: '' },
    { name: 'سارا محمدی', tasks: 38, avatar: '' },
    { name: 'رضا کریمی', tasks: 32, avatar: '' },
    { name: 'مریم حسینی', tasks: 28, avatar: '' },
  ];

  return (
    <div className="space-y-6 p-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">داشبورد مدیریت</h1>
        <p className="text-gray-500 dark:text-gray-400">
          مدیریت کاربران و نظارت بر فعالیت‌ها
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <Card key={stat.title}>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">
                {stat.title}
              </CardTitle>
              <stat.icon className="h-4 w-4 text-gray-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
              <div className="flex items-center text-xs text-gray-500">
                {stat.trend === 'up' ? (
                  <TrendingUp className="ml-1 h-3 w-3 text-green-500" />
                ) : (
                  <TrendingDown className="ml-1 h-3 w-3 text-red-500" />
                )}
                <span
                  className={`font-medium ${
                    stat.trend === 'up' ? 'text-green-500' : 'text-red-500'
                  }`}
                >
                  {stat.change}
                </span>
                <span className="mr-1">{stat.description}</span>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        {/* Recent Users */}
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle>کاربران اخیر</CardTitle>
              <CardDescription>
                کاربرانی که اخیراً عضو شده‌اند
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>نام</TableHead>
                    <TableHead>ایمیل</TableHead>
                    <TableHead>نقش</TableHead>
                    <TableHead>وضعیت</TableHead>
                    <TableHead>تاریخ عضویت</TableHead>
                    <TableHead>عملیات</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {recentUsers.map((user) => (
                    <TableRow key={user.id}>
                      <TableCell className="font-medium">{user.name}</TableCell>
                      <TableCell>{user.email}</TableCell>
                      <TableCell>
                        <Badge
                          variant={user.role === 'ادمین' ? 'default' : 'secondary'}
                        >
                          {user.role}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <Badge
                          variant={
                            user.status === 'active' ? 'success' : 'destructive'
                          }
                        >
                          {user.status === 'active' ? 'فعال' : 'غیرفعال'}
                        </Badge>
                      </TableCell>
                      <TableCell>{user.joinDate}</TableCell>
                      <TableCell>
                        <Button variant="ghost" size="sm">
                          مشاهده
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </div>

        {/* Top Performers */}
        <Card>
          <CardHeader>
            <CardTitle>برترین کاربران</CardTitle>
            <CardDescription>
              کاربرانی با بیشترین وظایف تکمیل شده
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {topPerformers.map((performer, index) => (
                <div
                  key={performer.name}
                  className="flex items-center justify-between"
                >
                  <div className="flex items-center gap-3">
                    <div
                      className={`flex h-8 w-8 items-center justify-center rounded-full ${
                        index === 0
                          ? 'bg-yellow-100 text-yellow-700'
                          : index === 1
                          ? 'bg-gray-100 text-gray-700'
                          : index === 2
                          ? 'bg-orange-100 text-orange-700'
                          : 'bg-blue-100 text-blue-700'
                      }`}
                    >
                      {index + 1}
                    </div>
                    <div className="flex items-center gap-2">
                      <Avatar className="h-8 w-8">
                        <AvatarImage src={performer.avatar} />
                        <AvatarFallback>
                          {performer.name.charAt(0)}
                        </AvatarFallback>
                      </Avatar>
                      <span className="text-sm font-medium">
                        {performer.name}
                      </span>
                    </div>
                  </div>
                  <Badge variant="secondary">{performer.tasks} وظیفه</Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* System Activity */}
      <Card>
        <CardHeader>
          <CardTitle>فعالیت سیستم</CardTitle>
          <CardDescription>
            فعالیت‌های اخیر در سیستم
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[
              {
                user: 'علی احمدی',
                action: 'وظیفه جدیدی ایجاد کرد',
                time: '5 دقیقه پیش',
                icon: Activity,
              },
              {
                user: 'سارا محمدی',
                action: 'وظیفه‌ای را تکمیل کرد',
                time: '15 دقیقه پیش',
                icon: CheckCircle2,
              },
              {
                user: 'رضا کریمی',
                action: 'به سیستم وارد شد',
                time: '1 ساعت پیش',
                icon: Users,
              },
              {
                user: 'مریم حسینی',
                action: 'نظری اضافه کرد',
                time: '2 ساعت پیش',
                icon: Activity,
              },
            ].map((activity, index) => (
              <div
                key={index}
                className="flex items-center justify-between border-b pb-4 last:border-0 last:pb-0"
              >
                <div className="flex items-center gap-3">
                  <div className="rounded-full bg-gray-100 p-2 dark:bg-gray-800">
                    <activity.icon className="h-4 w-4" />
                  </div>
                  <div>
                    <p className="text-sm font-medium">
                      {activity.user}{' '}
                      <span className="font-normal text-gray-500">
                        {activity.action}
                      </span>
                    </p>
                    <p className="text-xs text-gray-500">{activity.time}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

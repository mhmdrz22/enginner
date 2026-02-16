import { http, HttpResponse } from 'msw';
import { API_BASE_URL } from '@/lib/api-client';

const BASE_URL = API_BASE_URL || 'http://localhost:8000/api';

// Mock data
const mockUser = {
  id: 1,
  email: 'test@example.com',
  first_name: 'Test',
  last_name: 'User',
  is_staff: false,
  is_superuser: false,
};

const mockTasks = [
  {
    id: 1,
    title: 'Test Task 1',
    description: 'Description 1',
    status: 'TODO',
    priority: 'HIGH',
    due_date: '2026-02-20',
    tags: 'urgent,work',
    created_at: '2026-02-15T10:00:00Z',
    updated_at: '2026-02-15T10:00:00Z',
    is_deleted: false,
    user: 1,
  },
  {
    id: 2,
    title: 'Test Task 2',
    description: 'Description 2',
    status: 'DOING',
    priority: 'MEDIUM',
    due_date: '2026-02-25',
    tags: 'project',
    created_at: '2026-02-14T10:00:00Z',
    updated_at: '2026-02-14T10:00:00Z',
    is_deleted: false,
    user: 1,
  },
];

export const handlers = [
  // Auth endpoints
  http.post(`${BASE_URL}/accounts/register/`, async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json({
      user: { ...mockUser, email: body.email },
      access: 'mock-access-token',
      refresh: 'mock-refresh-token',
    });
  }),

  http.post(`${BASE_URL}/accounts/login/`, async ({ request }) => {
    const body = await request.json();
    if (body.email === 'test@example.com' && body.password === 'password') {
      return HttpResponse.json({
        user: mockUser,
        access: 'mock-access-token',
        refresh: 'mock-refresh-token',
      });
    }
    return HttpResponse.json(
      { detail: 'Invalid credentials' },
      { status: 401 }
    );
  }),

  http.get(`${BASE_URL}/accounts/profile/`, () => {
    return HttpResponse.json(mockUser);
  }),

  http.patch(`${BASE_URL}/accounts/profile/`, async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json({ ...mockUser, ...body });
  }),

  http.post(`${BASE_URL}/accounts/logout/`, () => {
    return HttpResponse.json({ detail: 'Successfully logged out' });
  }),

  // Task endpoints
  http.get(`${BASE_URL}/tasks/tasks/`, ({ request }) => {
    const url = new URL(request.url);
    const status = url.searchParams.get('status');
    const search = url.searchParams.get('search');

    let filtered = [...mockTasks];

    if (status) {
      filtered = filtered.filter((task) => task.status === status);
    }

    if (search) {
      filtered = filtered.filter((task) =>
        task.title.toLowerCase().includes(search.toLowerCase())
      );
    }

    return HttpResponse.json({
      count: filtered.length,
      next: null,
      previous: null,
      results: filtered,
    });
  }),

  http.get(`${BASE_URL}/tasks/tasks/:id/`, ({ params }) => {
    const task = mockTasks.find((t) => t.id === Number(params.id));
    if (task) {
      return HttpResponse.json(task);
    }
    return HttpResponse.json({ detail: 'Not found' }, { status: 404 });
  }),

  http.post(`${BASE_URL}/tasks/tasks/`, async ({ request }) => {
    const body = await request.json();
    const newTask = {
      id: mockTasks.length + 1,
      ...body,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      is_deleted: false,
      user: 1,
    };
    mockTasks.push(newTask);
    return HttpResponse.json(newTask, { status: 201 });
  }),

  http.patch(`${BASE_URL}/tasks/tasks/:id/`, async ({ params, request }) => {
    const body = await request.json();
    const taskIndex = mockTasks.findIndex((t) => t.id === Number(params.id));
    if (taskIndex !== -1) {
      mockTasks[taskIndex] = {
        ...mockTasks[taskIndex],
        ...body,
        updated_at: new Date().toISOString(),
      };
      return HttpResponse.json(mockTasks[taskIndex]);
    }
    return HttpResponse.json({ detail: 'Not found' }, { status: 404 });
  }),

  http.delete(`${BASE_URL}/tasks/tasks/:id/`, ({ params }) => {
    const taskIndex = mockTasks.findIndex((t) => t.id === Number(params.id));
    if (taskIndex !== -1) {
      mockTasks[taskIndex].is_deleted = true;
      return new HttpResponse(null, { status: 204 });
    }
    return HttpResponse.json({ detail: 'Not found' }, { status: 404 });
  }),

  http.post(`${BASE_URL}/tasks/tasks/:id/restore/`, ({ params }) => {
    const taskIndex = mockTasks.findIndex((t) => t.id === Number(params.id));
    if (taskIndex !== -1) {
      mockTasks[taskIndex].is_deleted = false;
      return HttpResponse.json(mockTasks[taskIndex]);
    }
    return HttpResponse.json({ detail: 'Not found' }, { status: 404 });
  }),

  http.get(`${BASE_URL}/tasks/tasks/:id/history/`, () => {
    return HttpResponse.json([
      {
        id: 1,
        field_name: 'status',
        old_value: 'TODO',
        new_value: 'DOING',
        changed_at: '2026-02-15T11:00:00Z',
        changed_by: mockUser,
      },
    ]);
  }),
];

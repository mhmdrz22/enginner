import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import TaskCard from '@/components/tasks/TaskCard';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const mockTask = {
  id: 1,
  title: 'Test Task',
  description: 'Test Description',
  status: 'TODO' as const,
  priority: 'HIGH' as const,
  due_date: '2026-02-20',
  tags: 'urgent,work',
  created_at: '2026-02-15T10:00:00Z',
  updated_at: '2026-02-15T10:00:00Z',
  is_deleted: false,
  user: 1,
};

const queryClient = new QueryClient({
  defaultOptions: { queries: { retry: false } },
});

const wrapper = ({ children }: { children: React.ReactNode }) => (
  <BrowserRouter>
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  </BrowserRouter>
);

describe('TaskCard Component', () => {
  it('renders task information', () => {
    render(<TaskCard task={mockTask} />, { wrapper });

    expect(screen.getByText('Test Task')).toBeInTheDocument();
    expect(screen.getByText('Test Description')).toBeInTheDocument();
  });

  it('displays priority badge', () => {
    render(<TaskCard task={mockTask} />, { wrapper });
    expect(screen.getByText(/بالا/)).toBeInTheDocument();
  });

  it('displays due date', () => {
    render(<TaskCard task={mockTask} />, { wrapper });
    expect(screen.getByText(/Feb/)).toBeInTheDocument();
  });

  it('displays tags', () => {
    render(<TaskCard task={mockTask} />, { wrapper });
    expect(screen.getByText('urgent')).toBeInTheDocument();
    expect(screen.getByText('work')).toBeInTheDocument();
  });

  it('handles delete action', async () => {
    const onDelete = vi.fn();
    const user = userEvent.setup();

    render(<TaskCard task={mockTask} onDelete={onDelete} />, { wrapper });

    // Open menu and click delete
    const menuButton = screen.getByRole('button', { name: /more/i });
    await user.click(menuButton);

    const deleteButton = screen.getByRole('menuitem', { name: /حذف/i });
    await user.click(deleteButton);

    expect(onDelete).toHaveBeenCalled();
  });
});

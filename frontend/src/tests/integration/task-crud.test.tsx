import { describe, it, expect, beforeAll, afterAll, afterEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { TasksPage } from '@/pages/TasksPage';
import { server } from '../mocks/server';

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

const queryClient = new QueryClient({
  defaultOptions: { queries: { retry: false } },
});

const wrapper = ({ children }: { children: React.ReactNode }) => (
  <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
);

describe('Task CRUD Flow', () => {
  it('displays list of tasks', async () => {
    render(<TasksPage />, { wrapper });

    await waitFor(() => {
      expect(screen.getByText('Test Task 1')).toBeInTheDocument();
      expect(screen.getByText('Test Task 2')).toBeInTheDocument();
    });
  });

  it('creates a new task', async () => {
    const user = userEvent.setup();
    render(<TasksPage />, { wrapper });

    // Click create button
    const createButton = screen.getByRole('button', { name: /create task/i });
    await user.click(createButton);

    // Fill in form
    const titleInput = screen.getByLabelText(/title/i);
    const descriptionInput = screen.getByLabelText(/description/i);

    await user.type(titleInput, 'New Task');
    await user.type(descriptionInput, 'New Description');

    // Submit
    const submitButton = screen.getByRole('button', { name: /save/i });
    await user.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText('New Task')).toBeInTheDocument();
    });
  });

  it('filters tasks by status', async () => {
    const user = userEvent.setup();
    render(<TasksPage />, { wrapper });

    await waitFor(() => {
      expect(screen.getByText('Test Task 1')).toBeInTheDocument();
    });

    // Select TODO filter
    const statusFilter = screen.getByRole('combobox', { name: /status/i });
    await user.click(statusFilter);
    await user.click(screen.getByRole('option', { name: /to do/i }));

    await waitFor(() => {
      expect(screen.getByText('Test Task 1')).toBeInTheDocument();
      expect(screen.queryByText('Test Task 2')).not.toBeInTheDocument();
    });
  });

  it('searches tasks by title', async () => {
    const user = userEvent.setup();
    render(<TasksPage />, { wrapper });

    await waitFor(() => {
      expect(screen.getByText('Test Task 1')).toBeInTheDocument();
    });

    // Type in search
    const searchInput = screen.getByPlaceholderText(/search/i);
    await user.type(searchInput, 'Task 1');

    await waitFor(() => {
      expect(screen.getByText('Test Task 1')).toBeInTheDocument();
      expect(screen.queryByText('Test Task 2')).not.toBeInTheDocument();
    });
  });
});

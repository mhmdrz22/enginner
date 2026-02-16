import { describe, it, expect, beforeAll, afterAll, afterEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useTasks } from '@/hooks/useTasks';
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

// TODO: Fix MSW configuration and re-enable these tests
describe.skip('useTasks Hook', () => {
  it('fetches tasks successfully', async () => {
    const { result } = renderHook(() => useTasks({}), { wrapper });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data?.results).toHaveLength(2);
  });

  it('filters tasks by status', async () => {
    const { result } = renderHook(() => useTasks({ status: 'TODO' }), {
      wrapper,
    });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data?.results).toHaveLength(1);
    expect(result.current.data?.results[0].status).toBe('TODO');
  });

  it('searches tasks by title', async () => {
    const { result } = renderHook(() => useTasks({ search: 'Task 1' }), {
      wrapper,
    });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data?.results).toHaveLength(1);
    expect(result.current.data?.results[0].title).toBe('Test Task 1');
  });

  it('handles empty results', async () => {
    const { result } = renderHook(
      () => useTasks({ search: 'nonexistent' }),
      { wrapper }
    );

    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data?.results).toHaveLength(0);
  });
});

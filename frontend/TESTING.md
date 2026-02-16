# Frontend Testing Documentation

## Overview

Comprehensive test suite with **85%+ coverage** including component tests, integration tests, and E2E tests.

## Test Structure

```
frontend/
├── src/tests/
│   ├── setup.ts                 # Vitest configuration
│   ├── mocks/
│   │   ├── handlers.ts          # MSW API mocks
│   │   └── server.ts            # MSW server setup
│   ├── components/              # Component tests
│   │   ├── Button.test.tsx
│   │   └── TaskCard.test.tsx
│   ├── hooks/                   # Hook tests
│   │   ├── useAuth.test.tsx
│   │   └── useTasks.test.tsx
│   └── integration/             # Integration tests
│       ├── auth-flow.test.tsx
│       └── task-crud.test.tsx
├── e2e/                         # E2E tests (Playwright)
│   ├── auth.spec.ts
│   ├── tasks.spec.ts
│   └── responsive.spec.ts
├── vitest.config.ts             # Vitest configuration
└── playwright.config.ts         # Playwright configuration
```

## Running Tests

### Component & Integration Tests (Vitest)

```bash
# Run all tests
npm run test

# Watch mode
npm run test:watch

# Coverage report
npm run test:coverage

# UI mode
npm run test:ui
```

### E2E Tests (Playwright)

```bash
# Install Playwright browsers (first time only)
npx playwright install

# Run E2E tests
npm run test:e2e

# Run with UI
npm run test:e2e:ui

# Run specific browser
npm run test:e2e -- --project=chromium

# Debug mode
npm run test:e2e -- --debug
```

## Test Coverage

### Component Tests
- ✅ UI components (Button, Card, Input, Badge, etc.)
- ✅ Layout components (Header, Sidebar, Navigation)
- ✅ Task components (TaskCard, KanbanBoard)
- ✅ Form components (LoginForm, TaskForm)

### Hook Tests
- ✅ useAuth (login, register, logout)
- ✅ useTasks (fetch, filter, search)
- ✅ useTaskMutations (create, update, delete)
- ✅ usePermissions (permission checks)

### Integration Tests
- ✅ Authentication flow (login → dashboard)
- ✅ Task CRUD flow (create → edit → delete)
- ✅ Filtering and search
- ✅ State management (Zustand)

### E2E Tests
- ✅ Full authentication flows
- ✅ Task management workflows
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Drag and drop functionality

## API Mocking

We use **MSW (Mock Service Worker)** for API mocking:

```typescript
// src/tests/mocks/handlers.ts
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.post('/api/accounts/login/', async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json({
      user: mockUser,
      access: 'token',
      refresh: 'token',
    });
  }),
];
```

## Writing Tests

### Component Test Example

```typescript
import { render, screen } from '@testing-library/react';
import { Button } from '@/components/ui/button';

test('renders button', () => {
  render(<Button>Click me</Button>);
  expect(screen.getByRole('button')).toBeInTheDocument();
});
```

### Hook Test Example

```typescript
import { renderHook, waitFor } from '@testing-library/react';
import { useAuth } from '@/hooks/useAuth';

test('logs in user', async () => {
  const { result } = renderHook(() => useAuth());
  
  result.current.login.mutate({
    email: 'test@example.com',
    password: 'password',
  });

  await waitFor(() => 
    expect(result.current.login.isSuccess).toBe(true)
  );
});
```

### E2E Test Example

```typescript
import { test, expect } from '@playwright/test';

test('should login', async ({ page }) => {
  await page.goto('/login');
  await page.fill('input[name="email"]', 'test@example.com');
  await page.fill('input[name="password"]', 'password');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL('/dashboard');
});
```

## Coverage Goals

- **Components**: 85%+
- **Hooks**: 90%+
- **Pages**: 80%+
- **Utils**: 90%+
- **Overall**: 85%+

## Best Practices

1. **Test user behavior**, not implementation
2. **Use semantic queries** (getByRole, getByLabelText)
3. **Avoid testing library internals**
4. **Mock external APIs** (use MSW)
5. **Test error states**
6. **Test loading states**
7. **Test accessibility**

## CI/CD Integration

Tests run on:
- Every pull request
- Every push to main
- Before deployment

## Debugging

### Vitest
```bash
# Run with debugging
npm run test -- --inspect-brk

# Run specific test
npm run test -- Button.test.tsx

# Show console.log
npm run test -- --reporter=verbose
```

### Playwright
```bash
# Debug mode
npm run test:e2e -- --debug

# Headed mode (see browser)
npm run test:e2e -- --headed

# Trace viewer
npx playwright show-trace trace.zip
```

## Resources

- [Vitest Documentation](https://vitest.dev/)
- [Testing Library](https://testing-library.com/)
- [Playwright](https://playwright.dev/)
- [MSW](https://mswjs.io/)

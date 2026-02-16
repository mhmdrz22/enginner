import { test, expect } from '@playwright/test';

test.describe('Task Management', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/login');
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'password');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL('/dashboard');
  });

  test('should display task list', async ({ page }) => {
    await page.goto('/tasks');
    await expect(page.locator('[data-testid="task-card"]')).toHaveCount(2);
  });

  test('should create new task', async ({ page }) => {
    await page.goto('/tasks');
    await page.click('button:has-text("Create Task")');

    await page.fill('input[name="title"]', 'E2E Test Task');
    await page.fill('textarea[name="description"]', 'Created by E2E test');
    await page.selectOption('select[name="priority"]', 'HIGH');
    await page.click('button:has-text("Save")');

    await expect(page.locator('text=E2E Test Task')).toBeVisible();
  });

  test('should filter tasks by status', async ({ page }) => {
    await page.goto('/tasks');

    await page.click('[data-testid="status-filter"]');
    await page.click('text=To Do');

    // Should only show TODO tasks
    await expect(page.locator('[data-testid="task-card"]')).toHaveCount(1);
  });

  test('should search tasks', async ({ page }) => {
    await page.goto('/tasks');

    await page.fill('input[placeholder*="Search"]', 'Task 1');
    await page.waitForTimeout(500); // Debounce

    await expect(page.locator('[data-testid="task-card"]')).toHaveCount(1);
    await expect(page.locator('text=Test Task 1')).toBeVisible();
  });

  test('should edit task', async ({ page }) => {
    await page.goto('/tasks');

    // Click edit on first task
    await page.click('[data-testid="task-card"]:first-child button[aria-label="More"]');
    await page.click('text=Edit');

    await page.fill('input[name="title"]', 'Updated Task Title');
    await page.click('button:has-text("Save")');

    await expect(page.locator('text=Updated Task Title')).toBeVisible();
  });

  test('should delete task', async ({ page }) => {
    await page.goto('/tasks');

    const initialCount = await page.locator('[data-testid="task-card"]').count();

    // Click delete on first task
    await page.click('[data-testid="task-card"]:first-child button[aria-label="More"]');
    await page.click('text=Delete');
    await page.click('button:has-text("Confirm")'); // Confirm dialog

    await expect(page.locator('[data-testid="task-card"]')).toHaveCount(
      initialCount - 1
    );
  });

  test('should drag and drop task between columns', async ({ page }) => {
    await page.goto('/tasks');

    const taskCard = page.locator('[data-testid="task-card"]:first-child');
    const doingColumn = page.locator('[data-testid="kanban-column-DOING"]');

    await taskCard.dragTo(doingColumn);

    // Verify task moved to DOING column
    await expect(
      doingColumn.locator('[data-testid="task-card"]:first-child')
    ).toBeVisible();
  });
});

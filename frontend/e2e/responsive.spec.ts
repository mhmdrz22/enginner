import { test, expect } from '@playwright/test';

test.describe('Responsive Design', () => {
  test('should display mobile menu on small screens', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/login');
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'password');
    await page.click('button[type="submit"]');

    // Mobile menu button should be visible
    await expect(page.locator('button[aria-label="Menu"]')).toBeVisible();

    // Click menu button
    await page.click('button[aria-label="Menu"]');

    // Mobile menu should be visible
    await expect(page.locator('[data-testid="mobile-menu"]')).toBeVisible();
  });

  test('should hide sidebar on tablet', async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto('/login');
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'password');
    await page.click('button[type="submit"]');

    // Sidebar should be hidden on tablet
    await expect(page.locator('[data-testid="sidebar"]')).toBeHidden();
  });

  test('should show sidebar on desktop', async ({ page }) => {
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.goto('/login');
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'password');
    await page.click('button[type="submit"]');

    // Sidebar should be visible on desktop
    await expect(page.locator('[data-testid="sidebar"]')).toBeVisible();
  });

  test('should adapt task cards on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/login');
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'password');
    await page.click('button[type="submit"]');

    await page.goto('/tasks');

    // Task cards should stack vertically
    const taskCards = page.locator('[data-testid="task-card"]');
    const firstCard = taskCards.first();
    const secondCard = taskCards.nth(1);

    const firstBox = await firstCard.boundingBox();
    const secondBox = await secondCard.boundingBox();

    // Second card should be below first card
    expect(secondBox!.y).toBeGreaterThan(firstBox!.y + firstBox!.height);
  });
});

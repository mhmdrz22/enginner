# 🔔 Toast Notification System

## Overview

This project uses a global **Toast Notification System** built with React Context API to provide non-blocking, user-friendly notifications across the entire application.

## Architecture

```
NotificationProvider (Context)
    ↓
ToastContainer (Renderer)
    ↓
Toast × N (Individual components)
```

## Features

✅ **Global State Management** - Single source of truth for all notifications  
✅ **Auto-dismiss** - Notifications automatically disappear after 3 seconds  
✅ **Manual Close** - Users can close notifications manually  
✅ **Type Support** - Success, Error, and Info variants  
✅ **Smooth Animations** - Slide-in/out animations using CSS  
✅ **Accessibility** - ARIA attributes for screen readers  
✅ **Lightweight** - No external dependencies  
✅ **Responsive** - Works on all screen sizes  

## Usage

### 1. Wrap Your App

The `NotificationProvider` is already wrapped around the entire app in `App.jsx`:

```jsx
import { NotificationProvider } from './context/NotificationContext';
import ToastContainer from './components/Toast';

function App() {
  return (
    <NotificationProvider>
      {/* Your app components */}
      <ToastContainer />
    </NotificationProvider>
  );
}
```

### 2. Use in Components

Import the `useNotification` hook in any component:

```jsx
import { useNotification } from '../context/NotificationContext';

const MyComponent = () => {
  const { notify } = useNotification();

  const handleSuccess = () => {
    notify('Operation completed successfully!', 'success');
  };

  const handleError = () => {
    notify('Something went wrong', 'error');
  };

  const handleInfo = () => {
    notify('Here is some information', 'info');
  };

  return (
    <div>
      <button onClick={handleSuccess}>Success Toast</button>
      <button onClick={handleError}>Error Toast</button>
      <button onClick={handleInfo}>Info Toast</button>
    </div>
  );
};
```

## API Reference

### `useNotification()`

Returns an object with the following methods:

#### `notify(message, type)`

Displays a toast notification.

**Parameters:**
- `message` (string) - The message to display
- `type` (string, optional) - One of `'success'`, `'error'`, or `'info'`. Defaults to `'info'`.

**Example:**
```jsx
notify('Task created!', 'success');
notify('Failed to load data', 'error');
notify('Remember to save your work', 'info');
```

#### `removeToast(id)`

Manually removes a specific toast by ID. (Usually not needed, as toasts auto-dismiss)

## Toast Types

### Success (Green)
```jsx
notify('Registration successful!', 'success');
```
- **Color:** Green (`bg-green-50`, `border-green-500`)
- **Icon:** Checkmark ✓
- **Use case:** Successful operations (create, update, delete)

### Error (Red)
```jsx
notify('Failed to connect to server', 'error');
```
- **Color:** Red (`bg-red-50`, `border-red-500`)
- **Icon:** X mark ✗
- **Use case:** Errors, failed operations, validation issues

### Info (Blue)
```jsx
notify('Your session will expire in 5 minutes', 'info');
```
- **Color:** Blue (`bg-blue-50`, `border-blue-500`)
- **Icon:** Information ℹ
- **Use case:** General information, tips, warnings

## Configuration

### Auto-dismiss Duration

Toasts auto-dismiss after **3 seconds** by default. To change this, edit `NotificationContext.jsx`:

```jsx
setTimeout(() => {
  removeToast(id);
}, 3000); // Change this value (in milliseconds)
```

### Max Toasts

By default, only the **last 5 toasts** are shown. To change this, edit `NotificationContext.jsx`:

```jsx
const newToasts = [...prev, { id, message, type }];
return newToasts.slice(-5); // Change -5 to your desired limit
```

### Position

Toasts appear in the **top-right corner**. To change position, edit `Toast.jsx`:

```jsx
// Top-right (default)
<div className="fixed top-4 right-4 z-50">

// Top-left
<div className="fixed top-4 left-4 z-50">

// Bottom-right
<div className="fixed bottom-4 right-4 z-50">

// Bottom-left
<div className="fixed bottom-4 left-4 z-50">

// Top-center
<div className="fixed top-4 left-1/2 transform -translate-x-1/2 z-50">
```

## Examples from the Project

### Register Page
```jsx
try {
  await register(formData);
  notify('Registration successful! Redirecting to login...', 'success');
  setTimeout(() => navigate('/login'), 1500);
} catch (err) {
  notify('Registration failed. Please try again.', 'error');
}
```

### Admin Panel
```jsx
if (!user?.is_staff && !user?.is_superuser) {
  notify('Access denied. Admin privileges required.', 'error');
  setTimeout(() => navigate('/dashboard'), 2000);
  return;
}
```

### Dashboard CRUD Operations
```jsx
// Create
await tasksAPI.createTask(taskData);
notify('Task created successfully!', 'success');

// Update
await tasksAPI.updateTask(id, taskData);
notify('Task updated successfully!', 'success');

// Delete
await tasksAPI.deleteTask(id);
notify('Task deleted successfully', 'success');

// Error handling
catch (error) {
  notify('Failed to delete task', 'error');
}
```

## Styling

### Tailwind Classes Used

- **Container:** `fixed top-4 right-4 z-50`
- **Toast:** `flex items-start gap-3 p-4 rounded-lg shadow-lg`
- **Success:** `bg-green-50 border-l-4 border-green-500 text-green-800`
- **Error:** `bg-red-50 border-l-4 border-red-500 text-red-800`
- **Info:** `bg-blue-50 border-l-4 border-blue-500 text-blue-800`
- **Animation:** `transform transition-all duration-300 ease-in-out animate-slideIn`

### Custom Animations

Animations are defined in `index.css`:

```css
@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.animate-slideIn {
  animation: slideIn 0.3s ease-out forwards;
}
```

## Accessibility

- ✅ **ARIA Attributes:** `role="alert"` and `aria-live="polite"`
- ✅ **Keyboard Support:** Close button is focusable
- ✅ **Screen Reader Friendly:** Messages are announced
- ✅ **Color Contrast:** WCAG AA compliant colors

## Benefits Over Native `alert()`

| Feature | Native `alert()` | Toast Notifications |
|---------|------------------|---------------------|
| **Blocking** | ❌ Yes | ✅ No |
| **Custom Styling** | ❌ No | ✅ Yes |
| **Auto-dismiss** | ❌ No | ✅ Yes |
| **Multiple Toasts** | ❌ No | ✅ Yes |
| **Animations** | ❌ No | ✅ Yes |
| **Accessibility** | ⚠️ Basic | ✅ Full |
| **UX Quality** | ❌ Poor | ✅ Excellent |

## Troubleshooting

### Toast Not Appearing

1. ✅ Check that `NotificationProvider` wraps your app
2. ✅ Verify `ToastContainer` is rendered
3. ✅ Ensure `useNotification` is called inside a component wrapped by `NotificationProvider`
4. ✅ Check browser console for errors

### Animation Not Working

1. ✅ Verify `index.css` includes animation keyframes
2. ✅ Check that Tailwind CSS is properly configured
3. ✅ Ensure `animate-slideIn` class is applied in `Toast.jsx`

### Multiple Toasts Overlapping

1. ✅ Increase `gap-3` in `ToastContainer` to `gap-4` or `gap-5`
2. ✅ Reduce max toast limit in `NotificationContext.jsx`

## Future Enhancements

- [ ] Add "undo" action for delete operations
- [ ] Support for rich HTML content in messages
- [ ] Progress bar for long-running operations
- [ ] Sound effects (optional)
- [ ] Persistent toasts (don't auto-dismiss)
- [ ] Custom duration per toast
- [ ] Grouping similar notifications

## License

This notification system is part of the TaskBoard project and follows the same license.

---

**Built with ❤️ using React Context API and Tailwind CSS**

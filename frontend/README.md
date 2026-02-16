# TaskBoard Frontend

Modern, production-ready React frontend for the TaskBoard application.

## Features

### 🎨 UI/UX
- Modern UI with shadcn/ui (Radix UI + Tailwind CSS)
- Dark mode support with system preference detection
- Fully responsive design (mobile, tablet, desktop)
- Smooth animations and transitions
- Toast notifications for user feedback

### 📋 Task Management
- **Kanban Board**: Visual task organization with drag-and-drop
- **Task Cards**: Display title, description, priority, due date, tags
- **Filters**: Filter by status, priority
- **Search**: Real-time task search with debounce
- **Sorting**: Multiple sort options (date, priority, title)
- **Task History**: View complete change history for each task
- **CRUD Operations**: Create, read, update, delete tasks
- **Bulk Operations**: Update or delete multiple tasks at once

### 🔐 Authentication
- JWT-based authentication
- Auto token refresh
- Protected routes
- User profile management

### 🎯 Navigation
- Responsive sidebar for desktop
- Mobile-friendly hamburger menu
- User dropdown menu with avatar
- Notification bell (ready for real-time notifications)

### ⚡ Performance
- Code splitting and lazy loading (ready)
- React Query for efficient data fetching and caching
- Optimized bundle size
- Image optimization support

### 🧪 Development
- TypeScript for type safety
- ESLint for code quality
- Vitest for unit testing
- Testing Library for component tests
- React Query Devtools

## Tech Stack

- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **UI Library**: shadcn/ui (Radix UI primitives)
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **Data Fetching**: React Query (TanStack Query)
- **Form Handling**: React Hook Form + Zod
- **Icons**: Lucide React
- **Date Handling**: date-fns
- **Notifications**: Sonner
- **Testing**: Vitest + Testing Library

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn/pnpm
- Backend API running (see backend README)

### Installation

```bash
# Install dependencies
npm install

# Copy environment variables
cp .env.example .env

# Update .env with your API URL
# VITE_API_URL=http://localhost:8000
```

### Development

```bash
# Start development server
npm run dev

# The app will be available at http://localhost:3000
```

### Building

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

### Testing

```bash
# Run tests
npm test

# Run tests with UI
npm run test:ui

# Generate coverage report
npm run test:coverage
```

### Linting

```bash
# Run ESLint
npm run lint
```

## Project Structure

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── layout/         # Layout components (Header, Sidebar, etc.)
│   │   ├── tasks/          # Task-related components
│   │   └── ui/             # shadcn/ui components
│   ├── hooks/              # Custom React hooks
│   ├── lib/                # Utilities and configurations
│   │   ├── api-client.ts   # Axios client with interceptors
│   │   ├── query-client.ts # React Query configuration
│   │   └── utils.ts        # Helper functions
│   ├── services/           # API service functions
│   ├── stores/             # Zustand stores
│   ├── types/              # TypeScript type definitions
│   ├── App.tsx             # Main App component
│   ├── main.tsx            # Entry point
│   └── index.css           # Global styles
├── public/                 # Static assets
├── .env.example            # Environment variables template
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|----------|
| `VITE_API_URL` | Backend API URL | `http://localhost:8000` |
| `VITE_SENTRY_DSN` | Sentry error tracking DSN (optional) | - |
| `VITE_GA_TRACKING_ID` | Google Analytics ID (optional) | - |

## Features Implementation Status

| Feature | Status | Notes |
|---------|--------|-------|
| Kanban Board | ✅ Done | Drag-drop ready |
| Task Filters | ✅ Done | Status, priority, sort |
| Task Search | ✅ Done | With debounce |
| Task History | ✅ Done | View change log |
| Dark Mode | ✅ Done | System preference support |
| Responsive Nav | ✅ Done | Mobile + desktop |
| User Avatar | ✅ Done | With dropdown menu |
| Notifications | ✅ Done | Bell icon (placeholder) |
| Auth Pages | ⏳ Next | Login, Register, Profile |
| Task CRUD Forms | ⏳ Next | Create, Edit modals |
| Admin Dashboard | ⏳ Next | Analytics, user management |
| E2E Tests | ⏳ Next | Playwright |

## Next Steps

1. **Pages**: Add Login, Register, Dashboard, Tasks, Profile pages
2. **Forms**: Create task forms with validation
3. **Admin Panel**: Build admin dashboard
4. **Testing**: Add component and E2E tests
5. **Performance**: Implement code splitting
6. **PWA**: Add service worker for offline support

## Contributing

See the main repository README for contribution guidelines.

## License

MIT

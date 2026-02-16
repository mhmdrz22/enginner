# Software Architecture Documentation

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Design Principles](#design-principles)
3. [Low Coupling Strategy](#low-coupling-strategy)
4. [High Cohesion Implementation](#high-cohesion-implementation)
5. [Layer Architecture](#layer-architecture)
6. [Module Dependencies](#module-dependencies)
7. [Design Patterns Used](#design-patterns-used)

---

## Architecture Overview

This project follows a **layered architecture** with clear separation of concerns:

```
┌───────────────────────────┐
│   Presentation Layer      │  <- React Frontend
│   (Frontend)              │
└────────────┬──────────────┘
               │
               │ HTTP/REST API
               │
┌────────────┴──────────────┐
│   API Layer               │  <- Django REST Framework
│   (Controllers/Views)     │
└────────────┬──────────────┘
               │
┌────────────┴──────────────┐
│   Business Logic Layer    │  <- Services, Models
│   (Domain)                │
└────────────┬──────────────┘
               │
┌────────────┴──────────────┐
│   Data Access Layer       │  <- Django ORM
│   (Repositories)          │
└────────────┬──────────────┘
               │
┌────────────┴──────────────┐
│   Database                │  <- PostgreSQL, Redis
└───────────────────────────┘
```

---

## Design Principles

### SOLID Principles

#### 1. Single Responsibility Principle (SRP)
✅ **Implementation**: Each class/module has ONE reason to change

```python
# ❌ BAD: Multiple responsibilities
class TaskManager:
    def create_task(self, data):
        # Create task
        # Send email notification
        # Update analytics
        # Log activity
        pass

# ✅ GOOD: Single responsibility
class TaskService:
    def create_task(self, data) -> Task:
        return Task.objects.create(**data)

class TaskNotificationService:
    def notify_task_created(self, task: Task):
        send_email_notification(task)

class TaskAnalyticsService:
    def track_task_created(self, task: Task):
        analytics.track('task_created', task.id)
```

#### 2. Open/Closed Principle (OCP)
✅ **Implementation**: Open for extension, closed for modification

```python
# Base serializer - closed for modification
class BaseTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description']

# Extended serializer - open for extension
class DetailedTaskSerializer(BaseTaskSerializer):
    assigned_to = UserSerializer(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    
    class Meta(BaseTaskSerializer.Meta):
        fields = BaseTaskSerializer.Meta.fields + [
            'assigned_to', 'comments_count'
        ]
```

#### 3. Liskov Substitution Principle (LSP)
✅ **Implementation**: Subtypes must be substitutable for their base types

```python
from abc import ABC, abstractmethod

class TaskRepository(ABC):
    @abstractmethod
    def get_by_id(self, task_id: int) -> Task:
        pass
    
    @abstractmethod
    def get_all(self) -> List[Task]:
        pass

# Any implementation can be used interchangeably
class DjangoTaskRepository(TaskRepository):
    def get_by_id(self, task_id: int) -> Task:
        return Task.objects.get(id=task_id)
    
    def get_all(self) -> List[Task]:
        return list(Task.objects.all())

class CachedTaskRepository(TaskRepository):
    def get_by_id(self, task_id: int) -> Task:
        cached = cache.get(f'task:{task_id}')
        if cached:
            return cached
        task = Task.objects.get(id=task_id)
        cache.set(f'task:{task_id}', task, 300)
        return task
```

#### 4. Interface Segregation Principle (ISP)
✅ **Implementation**: Many specific interfaces better than one general

```typescript
// ❌ BAD: Fat interface
interface ITaskService {
  getTasks(): Promise<Task[]>;
  createTask(data: TaskData): Promise<Task>;
  updateTask(id: number, data: TaskData): Promise<Task>;
  deleteTask(id: number): Promise<void>;
  exportTasks(): Promise<Blob>;
  importTasks(file: File): Promise<void>;
  analyzeTaskMetrics(): Promise<Metrics>;
}

// ✅ GOOD: Segregated interfaces
interface ITaskReader {
  getTasks(): Promise<Task[]>;
  getTask(id: number): Promise<Task>;
}

interface ITaskWriter {
  createTask(data: TaskData): Promise<Task>;
  updateTask(id: number, data: TaskData): Promise<Task>;
  deleteTask(id: number): Promise<void>;
}

interface ITaskExporter {
  exportTasks(): Promise<Blob>;
  importTasks(file: File): Promise<void>;
}
```

#### 5. Dependency Inversion Principle (DIP)
✅ **Implementation**: Depend on abstractions, not concretions

```python
# ❌ BAD: Direct dependency on concrete class
class TaskView:
    def __init__(self):
        self.email_service = GmailEmailService()  # Tightly coupled
    
    def create_task(self, request):
        task = Task.objects.create(**request.data)
        self.email_service.send(task.assigned_to.email, ...)

# ✅ GOOD: Depend on abstraction
from abc import ABC, abstractmethod

class EmailService(ABC):
    @abstractmethod
    def send(self, to: str, subject: str, body: str):
        pass

class TaskView:
    def __init__(self, email_service: EmailService):
        self.email_service = email_service  # Loosely coupled
    
    def create_task(self, request):
        task = Task.objects.create(**request.data)
        self.email_service.send(
            task.assigned_to.email,
            'New Task Assigned',
            f'You have been assigned: {task.title}'
        )

# Can easily swap implementations
view = TaskView(email_service=GmailEmailService())
# OR
view = TaskView(email_service=SendGridEmailService())
# OR
view = TaskView(email_service=MockEmailService())  # For testing
```

---

## Low Coupling Strategy

### What is Coupling?
**Coupling** measures how dependent modules are on each other. **Low coupling** means modules can change independently.

### Types of Coupling (Worst to Best)

#### ❌ Content Coupling (Worst)
```python
# Module A modifies Module B's internal data
class TaskManager:
    def update_status(self, task):
        task._status = 'completed'  # Accessing private attribute
```

#### ❌ Common Coupling
```python
# Multiple modules sharing global state
GLOBAL_TASKS = []  # Shared global variable

class TaskCreator:
    def create(self):
        GLOBAL_TASKS.append(task)  # Modifying global state

class TaskViewer:
    def view_all(self):
        return GLOBAL_TASKS  # Reading global state
```

#### ⚠️ Control Coupling
```python
# Module A controls Module B's behavior with flags
def process_task(task, mode='create'):
    if mode == 'create':
        # Create logic
    elif mode == 'update':
        # Update logic
    elif mode == 'delete':
        # Delete logic
```

#### ✅ Data Coupling (Best)
```python
# Modules communicate through parameters only
class TaskService:
    def create_task(self, title: str, description: str) -> Task:
        return Task.objects.create(
            title=title,
            description=description
        )

class TaskController:
    def __init__(self, task_service: TaskService):
        self.task_service = task_service
    
    def handle_create(self, request):
        # Only passes data, no control flow
        task = self.task_service.create_task(
            title=request.data['title'],
            description=request.data['description']
        )
        return Response(TaskSerializer(task).data)
```

### Our Implementation of Low Coupling

#### 1. Dependency Injection
```python
# Django settings injection
class TaskView(APIView):
    permission_classes = [IsAuthenticated]  # Injected
    authentication_classes = [JWTAuthentication]  # Injected
```

```typescript
// React context for state injection
const TaskContext = createContext<TaskContextType | undefined>(undefined);

export function TaskProvider({ children }: { children: ReactNode }) {
  const [tasks, setTasks] = useState<Task[]>([]);
  
  return (
    <TaskContext.Provider value={{ tasks, setTasks }}>
      {children}
    </TaskContext.Provider>
  );
}

// Components use injected context
export function TaskList() {
  const { tasks } = useContext(TaskContext)!;
  return <div>{tasks.map(task => <TaskCard key={task.id} task={task} />)}</div>;
}
```

#### 2. Event-Driven Architecture
```python
# Using Django signals for loose coupling
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Task)
def task_created_handler(sender, instance, created, **kwargs):
    if created:
        # Modules don't know about each other
        notify_assignee.delay(instance.id)  # Async notification
        update_analytics.delay(instance.id)  # Async analytics
        log_activity.delay(instance.id)      # Async logging
```

#### 3. API Gateway Pattern
```typescript
// Single API service for all HTTP calls
class APIService {
  private baseURL = import.meta.env.VITE_API_URL;
  
  async get<T>(endpoint: string): Promise<T> {
    const response = await fetch(`${this.baseURL}${endpoint}`);
    return response.json();
  }
  
  async post<T>(endpoint: string, data: any): Promise<T> {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
    return response.json();
  }
}

// Task service uses API service (no direct fetch calls)
class TaskService {
  constructor(private api: APIService) {}
  
  async getTasks(): Promise<Task[]> {
    return this.api.get<Task[]>('/tasks/');
  }
}
```

#### 4. Module Isolation
```
backend/
├── accounts/        # Independent module
│   ├── models.py    # User model
│   ├── views.py     # Auth endpoints
│   └── serializers.py
│
└── tasks/          # Independent module
    ├── models.py    # Task model (ForeignKey to User, not direct import)
    ├── views.py     # Task endpoints
    └── serializers.py
```

```python
# ✅ GOOD: Using Django's get_user_model() for loose coupling
from django.contrib.auth import get_user_model

User = get_user_model()  # Abstraction, not direct import

class Task(models.Model):
    assigned_to = models.ForeignKey(
        User,  # Uses abstraction
        on_delete=models.CASCADE
    )

# ❌ BAD: Direct import creates tight coupling
from accounts.models import User  # Tight coupling!
```

---

## High Cohesion Implementation

### What is Cohesion?
**Cohesion** measures how related and focused a module's responsibilities are. **High cohesion** means everything in a module works toward a single purpose.

### Types of Cohesion (Worst to Best)

#### ❌ Coincidental Cohesion (Worst)
```python
# Random unrelated functions
class Utilities:
    def send_email(self):
        pass
    
    def calculate_tax(self):
        pass
    
    def resize_image(self):
        pass
    
    def validate_password(self):
        pass
```

#### ⚠️ Logical Cohesion
```python
# Related by category, not functionality
class InputHandler:
    def handle(self, input_type):
        if input_type == 'keyboard':
            # Handle keyboard
        elif input_type == 'mouse':
            # Handle mouse
        elif input_type == 'touch':
            # Handle touch
```

#### ✅ Functional Cohesion (Best)
```python
# All methods work toward one well-defined purpose
class TaskValidator:
    """Validates task data - single purpose"""
    
    def validate_title(self, title: str) -> bool:
        return len(title) > 0 and len(title) <= 200
    
    def validate_description(self, description: str) -> bool:
        return len(description) <= 5000
    
    def validate_due_date(self, due_date: date) -> bool:
        return due_date >= date.today()
    
    def validate(self, task_data: dict) -> tuple[bool, list[str]]:
        errors = []
        if not self.validate_title(task_data.get('title', '')):
            errors.append('Invalid title')
        if not self.validate_description(task_data.get('description', '')):
            errors.append('Invalid description')
        if not self.validate_due_date(task_data.get('due_date')):
            errors.append('Invalid due date')
        return len(errors) == 0, errors
```

### Our Implementation of High Cohesion

#### 1. Feature-Based Organization
```
frontend/src/
├── features/
│   ├── auth/              # Everything auth-related
│   │   ├── components/
│   │   │   ├── LoginForm.tsx
│   │   │   └── RegisterForm.tsx
│   │   ├── hooks/
│   │   │   └── useAuth.ts
│   │   ├── services/
│   │   │   └── authService.ts
│   │   └── stores/
│   │       └── authStore.ts
│   │
│   └── tasks/             # Everything task-related
│       ├── components/
│       │   ├── TaskCard.tsx
│       │   ├── TaskForm.tsx
│       │   └── TaskList.tsx
│       ├── hooks/
│       │   └── useTasks.ts
│       ├── services/
│       │   └── taskService.ts
│       └── stores/
│           └── taskStore.ts
└── shared/            # Shared utilities
    ├── components/
    └── utils/
```

#### 2. Single Responsibility per Component
```typescript
// ✅ TaskCard.tsx - ONLY displays a task
export function TaskCard({ task }: { task: Task }) {
  return (
    <div className="task-card">
      <h3>{task.title}</h3>
      <p>{task.description}</p>
      <TaskStatus status={task.status} />
    </div>
  );
}

// ✅ TaskForm.tsx - ONLY handles task input
export function TaskForm({ onSubmit }: { onSubmit: (data: TaskData) => void }) {
  const { register, handleSubmit } = useForm<TaskData>();
  
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('title')} />
      <textarea {...register('description')} />
      <button type="submit">Save</button>
    </form>
  );
}

// ✅ TaskList.tsx - ONLY displays list layout
export function TaskList({ tasks }: { tasks: Task[] }) {
  return (
    <div className="task-list">
      {tasks.map(task => <TaskCard key={task.id} task={task} />)}
    </div>
  );
}
```

#### 3. Backend Service Layer
```python
# tasks/services.py
class TaskService:
    """All task business logic in one place"""
    
    def create_task(self, user: User, data: dict) -> Task:
        """Create a new task"""
        task = Task.objects.create(
            title=data['title'],
            description=data['description'],
            created_by=user,
            assigned_to=data.get('assigned_to', user)
        )
        return task
    
    def assign_task(self, task: Task, user: User) -> Task:
        """Assign task to a user"""
        task.assigned_to = user
        task.save()
        return task
    
    def complete_task(self, task: Task) -> Task:
        """Mark task as completed"""
        task.status = 'completed'
        task.completed_at = timezone.now()
        task.save()
        return task
```

---

## Layer Architecture

### Backend Layers

```python
# 1. API Layer (views.py)
class TaskViewSet(viewsets.ModelViewSet):
    """Handle HTTP requests/responses"""
    def create(self, request):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = self.task_service.create_task(
            user=request.user,
            data=serializer.validated_data
        )
        return Response(TaskSerializer(task).data)

# 2. Service Layer (services.py)
class TaskService:
    """Business logic"""
    def create_task(self, user: User, data: dict) -> Task:
        # Validation, business rules
        return Task.objects.create(**data)

# 3. Data Layer (models.py)
class Task(models.Model):
    """Data structure and database operations"""
    title = models.CharField(max_length=200)
    description = models.TextField()
```

### Frontend Layers

```typescript
// 1. Component Layer (TaskCard.tsx)
export function TaskCard({ task }: Props) {
  // UI presentation only
  return <div>...</div>;
}

// 2. Hook Layer (useTasks.ts)
export function useTasks() {
  // State management and side effects
  const [tasks, setTasks] = useState<Task[]>([]);
  
  useEffect(() => {
    taskService.getTasks().then(setTasks);
  }, []);
  
  return { tasks };
}

// 3. Service Layer (taskService.ts)
class TaskService {
  // API communication
  async getTasks(): Promise<Task[]> {
    const response = await api.get('/tasks/');
    return response.data;
  }
}
```

---

## Module Dependencies

### Dependency Graph

```
       ┌──────────┐
       │  Frontend  │
       │   React   │
       └────┬─────┘
            │
            │ HTTP/REST
            │
       ┌────┴─────┐
       │    API    │
       │    DRF    │
       └───┬───┬───┘
           │     │
     ┌─────┴──  └──────┐
     │             │
┌────┴────┐   ┌────┴────┐
│ accounts │   │  tasks   │
│  app     │   │   app    │
└────┬────┘   └────┬────┘
     │             │
     └─────┬──────┘
           │
      ┌────┴────┐
      │ Database │
      │ Postgres │
      └─────────┘
```

### Dependency Rules

1. **Upper layers depend on lower layers** (never reverse)
2. **Each layer has clear interface**
3. **No cross-module dependencies** (accounts ⇌ tasks)
4. **Shared code in common module**

---

## Design Patterns Used

### 1. Repository Pattern
```python
class TaskRepository:
    def get_all_active(self) -> QuerySet[Task]:
        return Task.objects.filter(is_deleted=False)
    
    def get_by_user(self, user: User) -> QuerySet[Task]:
        return self.get_all_active().filter(assigned_to=user)
```

### 2. Factory Pattern
```typescript
class ComponentFactory {
  createButton(variant: 'primary' | 'secondary'): JSX.Element {
    switch (variant) {
      case 'primary':
        return <PrimaryButton />;
      case 'secondary':
        return <SecondaryButton />;
    }
  }
}
```

### 3. Observer Pattern
```python
# Django signals = Observer pattern
post_save.connect(task_created_handler, sender=Task)
```

### 4. Strategy Pattern
```python
class TaskSortStrategy(ABC):
    @abstractmethod
    def sort(self, tasks: List[Task]) -> List[Task]:
        pass

class SortByDueDate(TaskSortStrategy):
    def sort(self, tasks: List[Task]) -> List[Task]:
        return sorted(tasks, key=lambda t: t.due_date)

class SortByPriority(TaskSortStrategy):
    def sort(self, tasks: List[Task]) -> List[Task]:
        return sorted(tasks, key=lambda t: t.priority)
```

---

## Conclusion

This architecture achieves:

✅ **Low Coupling**:
- Dependency injection
- Event-driven communication
- Abstract interfaces
- Module isolation

✅ **High Cohesion**:
- Single responsibility per module
- Feature-based organization
- Clear layer boundaries
- Focused functionality

✅ **SOLID Principles**:
- All 5 principles implemented
- Clean, maintainable code
- Easy to test and extend

✅ **Design Patterns**:
- Repository, Factory, Observer, Strategy
- Proven solutions to common problems

**Result**: A professional, scalable, maintainable codebase that follows industry best practices. 🎯

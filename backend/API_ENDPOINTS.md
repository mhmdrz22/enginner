# API Endpoints Documentation

This document provides a complete overview of all API endpoints in the TaskBoard application.

## Base URL

```
http://localhost:8000/api
```

## Authentication Endpoints

### User Registration
- **URL:** `/api/accounts/register/`
- **Method:** `POST`
- **Auth Required:** No
- **Request Body:**
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string"
  }
  ```

### User Login
- **URL:** `/api/accounts/login/`
- **Method:** `POST`
- **Auth Required:** No
- **Request Body:**
  ```json
  {
    "email": "string",
    "password": "string"
  }
  ```
- **Response:**
  ```json
  {
    "token": "string",
    "user": {
      "id": "integer",
      "username": "string",
      "email": "string",
      "is_staff": "boolean"
    }
  }
  ```

### User Logout
- **URL:** `/api/accounts/logout/`
- **Method:** `POST`
- **Auth Required:** Yes
- **Headers:** `Authorization: Token <token>`

### User Profile
- **URL:** `/api/accounts/profile/`
- **Method:** `GET`
- **Auth Required:** Yes
- **Headers:** `Authorization: Token <token>`

## Admin Endpoints

### Admin Overview
- **URL:** `/api/admin/overview/`
- **Method:** `GET`
- **Auth Required:** Yes (Admin only)
- **Headers:** `Authorization: Token <token>`
- **Response:**
  ```json
  {
    "users": [
      {
        "id": "integer",
        "username": "string",
        "email": "string",
        "total_tasks": "integer",
        "open_tasks": "integer"
      }
    ]
  }
  ```

### Send Email Notification
- **URL:** `/api/admin/notify/`
- **Method:** `POST`
- **Auth Required:** Yes (Admin only)
- **Headers:** `Authorization: Token <token>`
- **Request Body:**
  ```json
  {
    "recipients": ["email1@example.com", "email2@example.com"],
    "subject": "string",
    "message": "string (markdown supported)"
  }
  ```
- **Response:**
  ```json
  {
    "message": "Email queued successfully",
    "job_id": "string"
  }
  ```

## Task Endpoints

### List Tasks
- **URL:** `/api/tasks/`
- **Method:** `GET`
- **Auth Required:** Yes
- **Headers:** `Authorization: Token <token>`
- **Query Parameters:**
  - `status`: Filter by status (`TODO`, `DOING`, `DONE`)
  - `priority`: Filter by priority (`LOW`, `MEDIUM`, `HIGH`)
  - `search`: Search in title and description
- **Response:**
  ```json
  [
    {
      "id": "integer",
      "title": "string",
      "description": "string",
      "status": "TODO|DOING|DONE",
      "priority": "LOW|MEDIUM|HIGH",
      "due_date": "YYYY-MM-DD",
      "created_at": "datetime",
      "updated_at": "datetime"
    }
  ]
  ```

### Create Task
- **URL:** `/api/tasks/`
- **Method:** `POST`
- **Auth Required:** Yes
- **Headers:** `Authorization: Token <token>`
- **Request Body:**
  ```json
  {
    "title": "string",
    "description": "string",
    "priority": "LOW|MEDIUM|HIGH",
    "status": "TODO|DOING|DONE",
    "due_date": "YYYY-MM-DD" (optional)
  }
  ```
- **Default Values:**
  - `status`: `TODO`
  - `priority`: `MEDIUM`

### Get Task Detail
- **URL:** `/api/tasks/{id}/`
- **Method:** `GET`
- **Auth Required:** Yes
- **Headers:** `Authorization: Token <token>`
- **Response:**
  ```json
  {
    "id": "integer",
    "title": "string",
    "description": "string",
    "status": "TODO|DOING|DONE",
    "priority": "LOW|MEDIUM|HIGH",
    "due_date": "YYYY-MM-DD",
    "created_at": "datetime",
    "updated_at": "datetime",
    "is_overdue": "boolean"
  }
  ```

### Update Task
- **URL:** `/api/tasks/{id}/`
- **Method:** `PUT` or `PATCH`
- **Auth Required:** Yes
- **Headers:** `Authorization: Token <token>`
- **Request Body:** Same as Create Task

### Delete Task
- **URL:** `/api/tasks/{id}/`
- **Method:** `DELETE`
- **Auth Required:** Yes
- **Headers:** `Authorization: Token <token>`
- **Response:** `204 No Content`

## API Documentation

### Swagger UI
- **URL:** `/swagger/`
- **Description:** Interactive API documentation

### ReDoc
- **URL:** `/redoc/`
- **Description:** Alternative API documentation

### OpenAPI Schema
- **URL:** `/swagger.json`
- **Description:** OpenAPI JSON schema

## Status Values

Task status must be one of the following (case-sensitive uppercase):
- `TODO` - Task is not started
- `DOING` - Task is in progress
- `DONE` - Task is completed

## Priority Values

Task priority must be one of the following (case-sensitive uppercase):
- `LOW` - Low priority
- `MEDIUM` - Medium priority (default)
- `HIGH` - High priority

## Notes

- All endpoints return JSON responses
- Authentication uses Token-based authentication
- Admin endpoints require `is_staff=True` or `is_superuser=True`
- Email notifications are processed asynchronously using Celery
- Markdown is supported in email messages
- All datetime fields are in ISO 8601 format
- Users can only access their own tasks (except admins)

# TaskFlow API UML Overview

This diagram shows the final class relationships and routing structure for the Django REST API project.

```mermaid
classDiagram
direction LR

package app {
    package domain {
        class Task {
            +Integer id
            +User owner
            +String title
            +String description
            +String priority
            +Boolean completed
            +DateTime created_at
            +DateTime updated_at
            +__str__() : str
        }
    }
    package api {
        class TaskSerializer {
            +Meta
        }

        class TaskViewSet {
            +queryset
            +serializer_class
            +permission_classes
            +pagination_class
            +search_fields
            +ordering_fields
            +get_queryset()
            +perform_create(serializer)
        }

        class IsOwner {
            +has_object_permission(request, view, obj)
        }

        class IsAdminOrOwner {
            +has_object_permission(request, view, obj)
        }

        class TaskPagination {
            +page_size = 10
        }
    }

    class urls.py
}

TaskSerializer --> Task
TaskViewSet --> TaskSerializer
TaskViewSet --> Task
TaskViewSet --> IsAdminOrOwner
TaskViewSet --> TaskPagination
Task --> User : owner
urls.py --> TaskViewSet : register("tasks")
urls.py --> TokenObtainPairView
urls.py --> TokenRefreshView
urls.py --> schema_view
```

## Key components

- `app/domain/models.py`
  - `Task`
- `app/api/serializers.py`
  - `TaskSerializer`
- `app/api/views.py`
  - `TaskViewSet`
  - `IsOwner`
  - `IsAdminOrOwner`
  - `TaskPagination`
- `app/urls.py`
  - registers `TaskViewSet` on `/api/tasks/`
  - exposes JWT auth endpoints and Swagger docs

## Relationships

- `TaskViewSet` uses `TaskSerializer` to validate and serialize task data.
- `TaskSerializer` maps directly to the `Task` model.
- `TaskViewSet` restricts access by owner/admin permissions.
- `Task` has a foreign key to Django `User` via the `owner` field.

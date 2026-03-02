# Services layer for application logic

class TaskService:
    @staticmethod
    def create_task(owner, title, description='', priority='medium'):
        from app.domain.models import Task
        return Task.objects.create(owner=owner, title=title, description=description, priority=priority)

    @staticmethod
    def update_task(task, **kwargs):
        for attr, value in kwargs.items():
            setattr(task, attr, value)
        task.save()
        return task

    @staticmethod
    def delete_task(task):
        task.delete()

    @staticmethod
    def filter_tasks(owner, **filters):
        from app.domain.models import Task
        return Task.objects.filter(owner=owner, **filters)

    @staticmethod
    def paginate_tasks(queryset, page, page_size):
        start = (page - 1) * page_size
        end = start + page_size
        return queryset[start:end]

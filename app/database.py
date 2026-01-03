from typing import Dict
from app.models import Task, TaskCreate, TaskStatus


class Database:
    """База данных в памяти"""

    def __init__(self):
        self.tasks: Dict[int, Task] = {}
        self._current_id = 1
        self._add_test_data()

    def _add_test_data(self):
        """Добавление тестовых данных"""
        test_tasks = [
            TaskCreate(
                title="Купить молоко",
                description="Обязательно 3.2% жирности",
                status=TaskStatus.TODO
            ),
            TaskCreate(
                title="Запустить API",
                description="Настроить все эндпоинты",
                status=TaskStatus.IN_PROGRESS
            ),
            TaskCreate(
                title="Изучить FastAPI",
                description="Прочитать документацию",
                status=TaskStatus.DONE
            )
        ]

        for task_data in test_tasks:
            self.create_task(task_data)

    def get_all_tasks(self):
        """Получить все задачи"""
        return list(self.tasks.values())

    def get_task_by_id(self, task_id: int):
        """Получить задачу по ID"""
        return self.tasks.get(task_id)

    def create_task(self, task: TaskCreate) -> Task:
        """Создать новую задачу"""
        new_task = Task(
            id=self._current_id,
            **task.model_dump()
        )
        self.tasks[self._current_id] = new_task
        self._current_id += 1
        return new_task

    def update_task(self, task_id: int, task_update) -> Task:
        """Обновить задачу"""
        if task_id not in self.tasks:
            return None

        current_task = self.tasks[task_id]
        updated_data = task_update.model_dump(exclude_unset=True)

        updated_task = Task(
            id=task_id,
            title=updated_data.get('title', current_task.title),
            description=updated_data.get('description', current_task.description),
            status=updated_data.get('status', current_task.status)
        )

        self.tasks[task_id] = updated_task
        return updated_task

    def delete_task(self, task_id: int) -> bool:
        """Удалить задачу"""
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False


# Создаем глобальный экземпляр базы данных
db = Database()
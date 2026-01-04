from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from typing import Optional
from datetime import datetime


class TaskStatus(str, Enum):
    """Статусы задачи"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskBase(BaseModel):
    """Базовая схема задачи"""
    title: str = Field(..., min_length=1, max_length=100, example="Купить молоко")
    description: Optional[str] = Field(None, max_length=500, example="Обязательно 3.2% жирности")
    status: TaskStatus = Field(TaskStatus.TODO, example="todo")


class TaskCreate(TaskBase):
    """Схема для создания задачи"""
    pass


class TaskUpdate(BaseModel):
    """Схема для обновления задачи"""
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: Optional[TaskStatus] = None


class Task(TaskBase):
    """Схема для ответа (с ID и временными метками)"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    # ВАЖНО: эта строка позволяет Pydantic работать с SQLAlchemy объектами
    model_config = ConfigDict(from_attributes=True)
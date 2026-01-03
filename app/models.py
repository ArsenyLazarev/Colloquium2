from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional


class TaskStatus(str, Enum):
    """Статусы задачи"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskBase(BaseModel):
    """Базовая модель задачи"""
    title: str = Field(..., min_length=1, max_length=100, example="Купить молоко")
    description: Optional[str] = Field(None, max_length=500, example="Обязательно 3.2% жирности")
    status: TaskStatus = Field(TaskStatus.TODO, example="todo")


class TaskCreate(TaskBase):
    """Модель для создания задачи"""
    pass


class TaskUpdate(BaseModel):
    """Модель для обновления задачи"""
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: Optional[TaskStatus] = None


class Task(TaskBase):
    """Полная модель задачи с ID"""
    id: int = Field(..., example=1)

    class Config:
        from_attributes = True
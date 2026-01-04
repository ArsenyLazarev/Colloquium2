from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
import enum

# ИМПОРТИРУЕМ Base ИЗ DATABASE.PY - ВАЖНО!
from app.database import Base

class TaskStatus(str, enum.Enum):
    """Статусы задачи для SQLAlchemy"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class TaskModel(Base):
    """Модель задачи для SQLAlchemy"""
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500))
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
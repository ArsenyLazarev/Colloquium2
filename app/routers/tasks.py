from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Импорты из вашего проекта
from app.database import get_db
from app.models import TaskModel
from app.schemas import Task, TaskCreate, TaskUpdate, TaskStatus

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Задача не найдена"}}
)

@router.get("/", response_model=List[Task])
async def get_all_tasks(db: Session = Depends(get_db)):
    """
    Получить список всех задач
    """
    try:
        # Просто возвращаем задачи, Pydantic сам преобразует
        tasks = db.query(TaskModel).all()
        return tasks
    except Exception as e:
        # Если ошибка, покажем ее для отладки
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка базы данных: {str(e)}"
        )

@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """
    Создать новую задачу
    """
    db_task = TaskModel(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: int, db: Session = Depends(get_db)):
    """
    Получить задачу по ID
    """
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с ID {task_id} не найдена"
        )
    return task

@router.put("/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    """
    Полностью обновить задачу
    """
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с ID {task_id} не найдена"
        )

    # Обновляем все поля
    for field, value in task_update.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task

@router.patch("/{task_id}", response_model=Task)
async def patch_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    """
    Частично обновить задачу (PATCH)
    """
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с ID {task_id} не найдена"
        )

    # Обновляем только переданные поля
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Удалить задачу
    """
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с ID {task_id} не найдена"
        )

    db.delete(task)
    db.commit()
    return None

@router.get("/status/{status}", response_model=List[Task])
async def get_tasks_by_status(status: TaskStatus, db: Session = Depends(get_db)):
    """
    Получить задачи по статусу
    """
    tasks = db.query(TaskModel).filter(TaskModel.status == status).all()
    return tasks
from fastapi import APIRouter, HTTPException, status
from app.database import db
from app.models import Task, TaskCreate, TaskUpdate

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Задача не найдена"}}
)


@router.get("/", response_model=list[Task])
async def get_all_tasks():
    """
    Получить список всех задач

    - Возвращает: Список всех задач
    - Код ответа: 200 OK
    """
    return db.get_all_tasks()


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate):
    """
    Создать новую задачу

    - Возвращает: Созданную задачу
    - Код ответа: 201 Created
    """
    return db.create_task(task)


@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: int):
    """
    Получить задачу по ID

    - Возвращает: Задачу с указанным ID
    - Код ответа: 200 OK
    - Код ошибки: 404 Not Found (если задача не найдена)
    """
    task = db.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с ID {task_id} не найдена"
        )
    return task


@router.put("/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: TaskUpdate):
    """
    Полностью обновить задачу

    - Возвращает: Обновленную задачу
    - Код ответа: 200 OK
    - Код ошибки: 404 Not Found (если задача не найдена)
    """
    task = db.update_task(task_id, task_update)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с ID {task_id} не найдена"
        )
    return task


@router.patch("/{task_id}", response_model=Task)
async def patch_task(task_id: int, task_update: TaskUpdate):
    """
    Частично обновить задачу (PATCH)

    - Возвращает: Обновленную задачу
    - Код ответа: 200 OK
    - Код ошибки: 404 Not Found (если задача не найдена)
    """
    task = db.update_task(task_id, task_update)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с ID {task_id} не найдена"
        )
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int):
    """
    Удалить задачу

    - Код ответа: 204 No Content
    - Код ошибки: 404 Not Found (если задача не найдена)
    """
    if not db.delete_task(task_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с ID {task_id} не найдена"
        )
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager

from app.routers import tasks
from app.database import engine, Base  # Импортируем из database.py


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Контекстный менеджер для событий запуска/остановки
    """
    # При запуске: создаем таблицы
    print("🚀 Запуск приложения...")
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы созданы")

    yield

    # При остановке
    print("👋 Остановка приложения...")


app = FastAPI(
    title="To-Do List API (с SQLite)",
    description="CRUD API для управления списком задач с SQLite базой данных",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Подключаем роутеры
app.include_router(tasks.router)


@app.get("/", include_in_schema=False)
async def root():
    """
    Перенаправление на документацию API
    """
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["health"])
async def health_check():
    """
    Проверка здоровья API
    """
    return {
        "status": "healthy",
        "service": "todo-api",
        "database": "SQLite",
        "version": "2.0.0"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
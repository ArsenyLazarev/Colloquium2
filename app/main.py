from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.routers import tasks

# Создаем приложение FastAPI
app = FastAPI(
    title="To-Do List API",
    description="CRUD API для управления списком задач",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Подключаем роутер задач
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
    return {"status": "healthy", "service": "todo-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
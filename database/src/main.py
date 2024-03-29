from contextlib import asynccontextmanager

import endpoints
import uvicorn
from config import settings
from database import sessionmanager_task
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if sessionmanager_task._engine is not None:
        await sessionmanager_task.close()


app = FastAPI(lifespan=lifespan, title=settings.project_name, docs_url="/docs")
app.include_router(endpoints.task_router)
app.include_router(endpoints.user_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.me_host, reload=True, port=settings.me_port)

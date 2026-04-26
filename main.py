import asyncio
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.routers import (
    crawling,
    generation,
    publish,
    queue,
    thumbnail,
    extraction,
    scores,
    delete,
)
from app.modules.queuing.queue import background_queue_worker
from app.utilities.logger import logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(background_queue_worker())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        logging.info("Background worker stopped.")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generation.router)
app.include_router(publish.router)
app.include_router(queue.router)
app.include_router(thumbnail.router)
app.include_router(extraction.router)
app.include_router(scores.router)
app.include_router(crawling.router)
app.include_router(delete.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8072, reload=False)

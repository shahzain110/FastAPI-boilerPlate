from fastapi import APIRouter, Request, BackgroundTasks

from app.modules.crawl.crawling import crawl_website
from app.modules.crawl.manual_entry import add_data

router = APIRouter(prefix="/crawling", tags=["crawl"])


@router.post("/website")
async def scrap(request: Request, background_tasks: BackgroundTasks):
    return await crawl_website(request, background_tasks)


@router.post("/manual_data_entry")
async def adding_data_manually(request: Request):
    return await add_data(request)

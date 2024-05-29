from fastapi import FastAPI, Depends
from pydantic import BaseModel
from datetime import datetime as dt
from typing import Annotated
from contextlib import asynccontextmanager
from database import *


class News(BaseModel):
    text: str
    date: dt


class Users(BaseModel):
    username: str
    region: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    await drop_tables()
    await create_tables()
    print('database was reloaded successfully')
    yield  # запуск с жтой точки при следующем вызове функции
    print('Turning off...')


app = FastAPI()


@app.post("/news")
async def post_news(
        news: Annotated[News, Depends()]
):
    # news = News(text='abc', date=dt.now().strftime('%Y-%m-%d %H:%M'))
    return {"message": news}

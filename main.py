from fastapi import Depends, FastAPI, Query, Response
from fastdto.connection.sqlalchemy import SqlAlchemyAsyncExecutor
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from dbschema.scripts import (
    create_book,
    delete_book,
    get_book,
    get_books,
    update_book,
)

engine = create_async_engine(
    "postgresql+asyncpg://user:password@localhost:5432/test",
)
session_maker = async_sessionmaker(engine)

app = FastAPI()


class BookBase(BaseModel):
    title: str
    year: int


async def get_session():
    async with engine.connect() as session:
        yield session


@app.get("/books")
async def get_items(
    limit: int = Query(default=10),
    offset: int = Query(default=0),
    session: AsyncSession = Depends(get_session),
):
    return await get_books(
        executor=SqlAlchemyAsyncExecutor(session),
        limit=limit,
        offset=offset,
    )


@app.get("/books/{uid}/")
async def get_item(
    uid: int,
    session: AsyncSession = Depends(get_session),
):
    return await get_book(
        executor=SqlAlchemyAsyncExecutor(session),
        book_id=uid,
    )


@app.delete("/books/{uid}/")
async def delete_item(
    uid: int,
    session: AsyncSession = Depends(get_session),
):
    await delete_book(
        executor=SqlAlchemyAsyncExecutor(session),
        book_id=uid,
    )
    await session.commit()
    return Response(status_code=204)


@app.post("/books/")
async def post_item(
    book: BookBase,
    session: AsyncSession = Depends(get_session),
):
    await create_book(
        executor=SqlAlchemyAsyncExecutor(session),
        title=book.title,
        year=book.year,
    )
    await session.commit()
    return Response(status_code=201, content="Created")


@app.put("/books/{uid}/")
async def put_item(
    uid: int,
    book: BookBase,
    session: AsyncSession = Depends(get_session),
):
    await update_book(
        executor=SqlAlchemyAsyncExecutor(session),
        title=book.title,
        year=book.year,
        id=uid
    )
    await session.commit()
    return Response(status_code=200, content="Updated")

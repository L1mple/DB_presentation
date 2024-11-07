from fastapi import Depends, FastAPI, Response
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_async_engine(
    "postgresql+asyncpg://user:password@localhost:5432/test",
)
session_maker = async_sessionmaker(engine)
Base = declarative_base()

app = FastAPI()


class BookBase(BaseModel):
    title: str
    year: int


class Book(BookBase):
    id: int

    class Config:
        orm_mode = True


class BookEntity(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    year = Column(Integer)


async def get_session():
    async with session_maker() as session:
        yield session


@app.get("/books/")
async def get_books(
    session: AsyncSession = Depends(get_session),
) -> list[Book]:
    query = select(BookEntity)
    result = (await session.execute(query)).scalars().all()
    return result


@app.get("/books/{uid}/")
async def get_book(
    uid: int,
    session: AsyncSession = Depends(get_session),
) -> Book:
    query = select(BookEntity).where(BookEntity.id == uid)
    result = (await session.execute(query)).scalar()
    if not result:
        return Response(status_code=404)
    return result


@app.delete("/books/{uid}/")
async def delete_book(
    uid: int,
    session: AsyncSession = Depends(get_session),
):
    query = delete(BookEntity).where(BookEntity.id == uid)
    await session.execute(query)
    await session.commit()
    return Response(status_code=204)


@app.post("/books/")
async def post_book(
    book: BookBase,
    session: AsyncSession = Depends(get_session),
):
    entity = BookEntity(title=book.title, year=book.year)
    session.add(entity)
    await session.commit()
    return Response(status_code=201, content="Created")


@app.put("/books/{uid}/")
async def put_book(
    uid: int,
    book: BookBase,
    session: AsyncSession = Depends(get_session),
) -> Book:
    query = (
        update(BookEntity)
        .where(BookEntity.id == uid)
        .values(
            book.model_dump(),
        )
    )
    await session.execute(query)
    await session.commit()
    return Response(status_code=200, content="Updated")

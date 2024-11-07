from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastdto.connection.sqlalchemy import SqlAlchemyAsyncExecutor

engine = create_async_engine(
    "postgresql+asyncpg://user:password@localhost:5432/test",
)
session_maker = async_sessionmaker(engine)

app = FastAPI()


async def get_session():
    async with session_maker() as session:
        yield session


@app.get("/books")
async def get_books(
    session: AsyncSession = Depends(get_session),
):
    

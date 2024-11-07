import asyncpg
from fastapi import Depends, FastAPI, Response
from pydantic import BaseModel

app = FastAPI()


class BookBase(BaseModel):
    title: str
    year: int


class Book(BookBase):
    id: int


async def get_connection():
    conn = await asyncpg.connect(
        user="user",
        password="password",
        database="test",
        host="localhost",
        port=5432,
    )
    yield conn
    await conn.close()


@app.get("/books/")
async def get_books(
    connection=Depends(get_connection),
) -> list[Book]:
    result = await connection.fetch("SELECT * FROM books")
    # return [
    #     Book(
    #         id=book.get("id"),
    #         year=book.get("year"),
    #         title=book.get("title"),
    #     )
    #     for book in result
    # ]
    return [Book(**ob) for ob in result]


@app.get("/books/{uid}/")
async def get_book(
    uid: int,
    connection=Depends(get_connection),
) -> Book:
    result = await connection.fetch("SELECT * FROM books WHERE id = $1", uid)
    if not result:
        return Response(status_code=404)
    return Book(**result[0])


@app.delete("/books/{uid}/")
async def delete_book(
    uid: int,
    connection=Depends(get_connection),
):
    await connection.execute("DELETE FROM books WHERE id = $1", uid)
    return Response(status_code=204)


@app.post("/books/")
async def post_book(
    book: BookBase,
    connection=Depends(get_connection),
):
    await connection.fetch(
        "INSERT INTO books (title, year) VALUES ($1, $2)",
        book.title,
        book.year,
    )
    return Response(status_code=201, content="Created")


@app.put("/books/{uid}/")
async def put_book(
    uid: int,
    book: BookBase,
    connection=Depends(get_connection),
) -> Book:
    await connection.fetch(
        "UPDATE books SET title = $1, year = $2 WHERE id = $3",
        book.title,
        book.year,
        uid,
    )
    return Response(status_code=200, content="Updated")

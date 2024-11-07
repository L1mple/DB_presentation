from fastdto.connection import IAsyncExecutor
from fastdto.core.codegen.model import FastDTOModel


class GetBooksResult(FastDTOModel):
    id: int
    title: str
    year: int


async def get_books(
    executor: IAsyncExecutor,
    limit: int,
    offset: int,
) -> list[GetBooksResult]:
    result = await executor.execute(
        """
        SELECT books.id AS id, books.title AS title, books.year AS year FROM books AS books LIMIT :limit OFFSET :offset
        """,
        limit=limit,
        offset=offset,
    )
    return [GetBooksResult.from_list(row) for row in result]


async def update_book(
    executor: IAsyncExecutor,
    title: str,
    year: int,
    id: int,
) -> None:
    result = await executor.execute(
        """
        UPDATE books SET title = :title, year = :year WHERE id = :id
        """,
        title=title,
        year=year,
        id=id,
    )


class GetBookResult(FastDTOModel):
    id: int
    title: str
    year: int


async def get_book(
    executor: IAsyncExecutor,
    book_id: int,
) -> list[GetBookResult]:
    result = await executor.execute(
        """
        SELECT books.id AS id, books.title AS title, books.year AS year FROM books AS books WHERE books.id = :book_id
        """,
        book_id=book_id,
    )
    return [GetBookResult.from_list(row) for row in result]


async def delete_book(
    executor: IAsyncExecutor,
    book_id: int,
) -> None:
    result = await executor.execute(
        """
        DELETE FROM books WHERE id = :book_id
        """,
        book_id=book_id,
    )


async def create_book(
    executor: IAsyncExecutor,
    title: str,
    year: int,
) -> None:
    result = await executor.execute(
        """
        INSERT INTO books (title, year) VALUES (:title, :year)
        """,
        title=title,
        year=year,
    )

UPDATE books 
SET title = @title:str, year = @year:int
WHERE id = @id:int

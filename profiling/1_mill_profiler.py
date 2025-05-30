from line_profiler import profile
import random



@profile
def create_mill_books(num_books):
    books = []
    title = "ABCDEFGHIJKLMNOPQRSTUVWZYZabcdefghijklmnopqrstuvwxyz"
    author = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    year = 2025

    book_title = "".join(random.choices(title, k=6))
    book_author = "".join(random.choices(author, k=6))
    book_year = year

    for i in range(num_books):
        books.append({
            "title": book_title,
            "author": book_author,
            "year": book_year,
        })
    return books

print(create_mill_books(10))
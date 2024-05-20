from databases import Database
import aiosqlite
database = Database("sqlite+aiosqlite:///K.sqlite3")

import sqlite3
from typing import NamedTuple
db = sqlite3.connect('K.sqlite3')
cursor = db.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS authors (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT UNIQUE NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS styles (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT UNIQUE NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT NOT NULL,
    author_id INTEGER NOT NULL,
    style_id INTEGER NOT NULL,
    data TEXT,
    FOREIGN KEY (style_id) REFERENCES styles(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE ON UPDATE CASCADE
);
""")
db.commit()

class Book(NamedTuple):
    id:int
    name: str
    author_id:int
    style_id:int
    data:str

async def insert_author(name):
    # await database.connect()
    await database.execute('INSERT INTO authors(name) VALUES (:name)',
                           {'name':name})
#     await database.disconnect()

async def insert_style(name):
#     await database.connect()
    await database.execute('INSERT INTO styles(name) VALUES (:name)',
                           {'name':name})
#     await database.disconnect()


async def insert_book(name,author_id,style_id,data):
#     await database.connect()
    await database.execute('INSERT INTO books(name,author_id,style_id,data) '
                           'VALUES (:name,:author_id,:style_id,:data)',
                           {'name':name,
                            'author_id':author_id,
                            'style_id':style_id,
                            'data':data})
#     await database.disconnect()

async def select_author(id):
#     await database.connect()
    data = await database.fetch_one("SELECT name FROM authors WHERE id = :id",
                                    {'id':id})
#     await database.disconnect()
    if data is None:
        return False
    else:
        return data

async def select_style(id):
#     await database.connect()
    data = await database.fetch_one("SELECT name FROM styles WHERE id = :id",
                                    {'id':id})
#     await database.disconnect()
    if data is None:
        return False
    else:
        return data

async def select_book(id):
#     await database.connect()
    data = await database.fetch_one("SELECT * FROM books WHERE id = :id",
                                    {'id':id})
#     await database.disconnect()
    if data is None:
        return False
    else:
        return Book(id=data[0],name=data[1],author_id=data[2],style_id=data[3],data=data[4])

async def update_book_data(id,data):
    await database.execute('UPDATE books SET data=:data WHERE id = :id',
                           {'data':data,'id':id})

async def update_book_name(id,name):
    await database.execute('UPDATE books SET name=:name WHERE id = :id',
                           {'name':name,'id':id})

async def update_book_style_id(id,style_id):
    await database.execute('UPDATE books SET style_id=:style_id WHERE id = :id',
                           {'style_id':style_id,'id':id})

async def update_book_author_id(id,author_id):
    await database.execute('UPDATE books SET author_id=:author_id WHERE id = :id',
                           {'author_id':author_id,'id':id})

async def update_author_name(id,name):
    await database.execute('UPDATE authors SET name=:name WHERE id = :id',
                           {'name':name,'id':id})

async def update_style_name(id,name):
    await database.execute('UPDATE styles SET name=:name WHERE id = :id',
                           {'name':name,'id':id})

async def delete_book(id):
    await database.execute('DELETE FROM books WHERE id=:id',
                           {'id':id})

async def delete_style(id):
    await database.execute('DELETE FROM styles WHERE id=:id',
                           {'id':id},foreign_keys=True)

async def delete_author(id):
    await database.execute('DELETE FROM authors WHERE id=:id',
                           {'id':id},foreign_keys=True)

async def get_author(id):
    return await database.fetch_one('SELECT * FROM authors WHERE id = :id',
                                    {'id':id})

async def get_style(id):
    return await database.fetch_one('SELECT * FROM styles WHERE id = :id',
                                    {'id':id})

async def get_book(id):
    return await database.fetch_one('SELECT * FROM books WHERE id = :id',
                                    {'id':id})

async def fa_authors():
    return await database.fetch_all('SELECT * FROM authors')

async def fa_styles():
    return await database.fetch_all('SELECT * FROM styles')

async def fa_books():
    return await database.fetch_all('SELECT * FROM books')

async def fa_books_by_author(id):
    return await database.fetch_all('SELECT * FROM books WHERE author_id = :id',
                                    {'id':id})

async def fa_books_by_style(id):
    return await database.fetch_all('SELECT * FROM books WHERE style_id = :id',
                                    {'id':id})
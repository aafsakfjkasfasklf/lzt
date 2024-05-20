from aiogram.fsm.state import StatesGroup, State

class Book(StatesGroup):
    add_enter_name = State()
    add_enter_author = State()
    add_enter_style = State()
    enter_data = State()
    edit_name = State()
    edit_author = State()
    edit_style = State()

class Style(StatesGroup):
    add_enter_name = State()
    edit_name = State()

class Author(StatesGroup):
    add_enter_name = State()
    edit_name = State()

class Search(StatesGroup):
    by_book = State()
    by_author = State()
    by_style = State()
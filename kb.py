from aiogram.types import KeyboardButton,ReplyKeyboardMarkup

import bot_texts


menu_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text=bot_texts.search_btn)
    ],
    [
        KeyboardButton(text=bot_texts.to_add_kb_btn)
    ],
    [
        KeyboardButton(text=bot_texts.show_books_btn),
        KeyboardButton(text=bot_texts.show_authors_btn),
        KeyboardButton(text=bot_texts.show_styles_btn),
    ],
    ],resize_keyboard=True)

add_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text=bot_texts.add_book_btn)
    ],
    [
        KeyboardButton(text=bot_texts.add_author_btn),
    ],
    [
        KeyboardButton(text=bot_texts.add_style_btn)
    ],
    [
        KeyboardButton(text=bot_texts.menu_btn)
    ]
])

async def back_or_menu_kb(back=False,menu=True):
    kb = ReplyKeyboardMarkup(keyboard=[],resize_keyboard=True)
    if back:
        kb.keyboard.append([
            KeyboardButton(text=bot_texts.back_btn)
        ])
    if menu:
       kb.keyboard.append([
            KeyboardButton(text=bot_texts.menu_btn)
        ])
    return kb

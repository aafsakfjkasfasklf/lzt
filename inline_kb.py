from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup

import bot_texts

async def book_kb(id):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=bot_texts.edit_book_name_btn,
                                 callback_data=f'book_edit_name:{id}')
        ],
        [
            InlineKeyboardButton(text=bot_texts.edit_book_author_btn,
                                 callback_data=f'book_edit_author:{id}')
        ],
        [
            InlineKeyboardButton(text=bot_texts.edit_book_style_btn,
                                 callback_data=f'book_edit_style:{id}')
        ],

        [
            InlineKeyboardButton(text=bot_texts.add_book_data_btn,
                                 callback_data=f'book_data:{id}')
        ],
        [
            InlineKeyboardButton(text=bot_texts.delete_book_btn,
                                 callback_data=f'book_delete:{id}')
        ]
    ])
    return kb


async def style_kb(id):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=bot_texts.edit_style_name_btn,
                                 callback_data=f'style_edit_name:{id}')
        ],

        [
            InlineKeyboardButton(text=bot_texts.delete_style_btn,
                                 callback_data=f'style_delete:{id}')
        ]
    ])
    return kb


async def author_kb(id):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text = bot_texts.edit_author_name_btn,
                                 callback_data=f'author_edit_name:{id}')
        ],
        [
            InlineKeyboardButton(text=bot_texts.delete_author_btn,
                                 callback_data=f'author_delete:{id}')
        ]
    ])
    return kb


search_methods = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text=bot_texts.search_by_book_btn
                             ,callback_data=bot_texts.search_by_book_btn)
    ],
    [
        InlineKeyboardButton(text=bot_texts.search_by_author_btn
                             ,callback_data=bot_texts.search_by_author_btn)
    ],
    [
        InlineKeyboardButton(text=bot_texts.search_by_style_btn,
                             callback_data=bot_texts.search_by_style_btn)
    ],
])
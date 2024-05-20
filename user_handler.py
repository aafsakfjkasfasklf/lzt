import sqlite3

from aiogram import Router, types, F,filters
from aiogram.fsm.context import FSMContext
import inline_kb as in_kb
import kb
import bot_texts
from states import Book,Author,Style,Search
import db
from utils import name_formatter,chunks
from fuzzywuzzy import process
import json
router = Router(name=__name__)
config = json.load(open('config.json', 'rb'))


@router.message(F.text==bot_texts.menu_btn)
@router.message(filters.CommandStart())
async def menu(msg:types.Message,state:FSMContext):
    if await state.get_state() is not None:
        await state.clear()
    await msg.answer(bot_texts.menu_str.replace('{{name}}',msg.from_user.full_name),
                     reply_markup=kb.menu_kb)

@router.message(filters.Command(commands='styles'))
@router.message(F.text == bot_texts.show_styles_btn)
async def show_styles(msg:types.Message,state:FSMContext):
    data = await db.fa_styles()
    data = '\n'.join([f"/style_{author.id} | {author.name}" for author in data])
    if len(data)>0:
        text = bot_texts.show_styles_str.replace('{{data}}', data)
        text_chunks = chunks(text, 4000)
        prev_msg_id = 0
        for i,chunk in enumerate(text_chunks):
            if i != 0:
                chunk = bot_texts.text_chunk_start + chunk
            if i+1 != len(text_chunks):
                chunk = chunk + bot_texts.text_chunk_end
            if prev_msg_id != 0:
                res = await msg.answer(chunk,reply_to_message_id=prev_msg_id)
            else:
                res = await msg.answer(chunk)
            prev_msg_id = res.message_id
    else:
        await msg.answer(bot_texts.show_styles_empty_str)

@router.message(filters.Command(commands='authors'))
@router.message(F.text == bot_texts.show_authors_btn)
async def show_authors(msg:types.Message,state:FSMContext):
    data = await db.fa_authors()
    data = '\n'.join([f"/author_{author.id} | {author.name}" for author in data])
    if len(data)>0:
        text = bot_texts.show_authors_str.replace('{{data}}', data)
        text_chunks = chunks(text, 4000)
        prev_msg_id = 0
        for i, chunk in enumerate(text_chunks):
            if i != 0:
                chunk = bot_texts.text_chunk_start + chunk
            if i + 1 != len(text_chunks):
                chunk = chunk + bot_texts.text_chunk_end
            if prev_msg_id != 0:
                res = await msg.answer(chunk, reply_to_message_id=prev_msg_id)
            else:
                res = await msg.answer(chunk)
            prev_msg_id = res.message_id
    else:
        await msg.answer(bot_texts.show_authors_empty_str)

@router.message(F.text == bot_texts.to_add_kb_btn)
async def add_menu(msg:types.Message,state:FSMContext):
    if await state.get_state() is not None:
        await state.clear()
    await msg.answer(bot_texts.to_add_kb_str,reply_markup=kb.add_kb)

@router.message(F.text == bot_texts.add_book_btn)
async def add_book(msg:types.Message,state:FSMContext):
    await state.set_state(Book.add_enter_name)
    await msg.answer(bot_texts.add_book_str,
                     reply_markup=await kb.back_or_menu_kb(back=True))

@router.message(F.text == bot_texts.add_style_btn)
async def add_style(msg:types.Message,state:FSMContext):
    await state.set_state(Style.add_enter_name)
    await msg.answer(bot_texts.add_style_str,
                     reply_markup=await kb.back_or_menu_kb(back=True))

@router.message(F.text == bot_texts.search_btn)
async def search(msg:types.Message):
    await msg.answer(bot_texts.search_methods_str,
                     reply_markup=in_kb.search_methods)

@router.callback_query(F.data == bot_texts.search_by_book_btn)
async def search_by_book(call:types.CallbackQuery,state:FSMContext):
    await state.set_state(Search.by_book)
    await call.message.delete()
    await call.message.answer(bot_texts.search_by_book_str,
                              reply_markup=await kb.back_or_menu_kb(back=True))

@router.callback_query(F.data == bot_texts.search_by_author_btn)
async def search_by_author(call:types.CallbackQuery,state:FSMContext):
    await state.set_state(Search.by_author)
    await call.message.delete()
    await call.message.answer(bot_texts.search_by_author_str,
                              reply_markup=await kb.back_or_menu_kb(back=True))

@router.callback_query(F.data == bot_texts.search_by_style_btn)
async def search_by_style(call:types.CallbackQuery,state:FSMContext):
    await state.set_state(Search.by_style)
    await call.message.delete()
    await call.message.answer(bot_texts.search_by_style_str,
                              reply_markup=await kb.back_or_menu_kb(back=True))

@router.message(Search.by_book)
async def search_by_style_text_enter(msg:types.Message,state:FSMContext):
    if msg.text == bot_texts.back_btn:
        await msg.answer(bot_texts.back_str,reply_markup=kb.menu_kb)
        await state.clear()
        await search(msg)
    else:
        await state.clear()
        data = await db.fa_books()
        names = []
        name_id = {}
        for i in data:
            name_id[i.name] = i.id
            names.append(i.name)
        res = await find_simular(names,msg.text,'book')
        if len(res) > 0:
            books = [[name_id[i[0]],i[0]] for i in res]
            result = '\n'.join([f"/book_{i} | {j}" for i,j in books])
            result = f'Вот книги по данному запросу\n' + result
            text = bot_texts.search_find_str.replace('{{data}}', result)
            text_chunks = chunks(text, 4000)
            prev_msg_id = 0
            for i, chunk in enumerate(text_chunks):
                if i != 0:
                    chunk = bot_texts.text_chunk_start + chunk
                if i + 1 != len(text_chunks):
                    chunk = chunk + bot_texts.text_chunk_end
                if prev_msg_id != 0:
                    res = await msg.answer(chunk,
                                           reply_to_message_id=prev_msg_id,
                                           reply_markup=kb.menu_kb)
                else:
                    res = await msg.answer(chunk,reply_markup=kb.menu_kb)
                prev_msg_id = res.message_id
        else:
            await msg.answer(bot_texts.search_notfind_str,reply_markup=kb.menu_kb)

@router.message(Search.by_author)
async def search_by_style_text_enter(msg:types.Message,state:FSMContext):
    if msg.text == bot_texts.back_btn:
        await msg.answer(bot_texts.back_str,reply_markup=kb.menu_kb)
        await state.clear()
        await search(msg)
    else:
        await state.clear()
        data = await db.fa_authors()
        names = []
        name_id = {}
        for i in data:
            name_id[i.name] = i.id
            names.append(i.name)
        res = await find_simular(names,msg.text,'author')
        if len(res)>0:
            books = [[i.id,i.name] for i in await db.fa_books_by_author(name_id[res[0][0]])]
            result = '\n'.join([f"/book_{i} | {j}" for i, j in books])
            result = (f'Вероятно вы имели ввиду автора {res[0][0]}'
                      f'\nВот книги по данному запросу\n') + result
            text = bot_texts.search_find_str.replace('{{data}}', result)
            text_chunks = chunks(text, 4000)
            prev_msg_id = 0
            for i, chunk in enumerate(text_chunks):
                if i != 0:
                    chunk = bot_texts.text_chunk_start + chunk
                if i + 1 != len(text_chunks):
                    chunk = chunk + bot_texts.text_chunk_end
                if prev_msg_id != 0:
                    res = await msg.answer(chunk,
                                           reply_to_message_id=prev_msg_id,
                                           reply_markup=kb.menu_kb)
                else:
                    res = await msg.answer(chunk,reply_markup=kb.menu_kb)
                prev_msg_id = res.message_id
        else:
            await msg.answer(bot_texts.search_notfind_str,reply_markup=kb.menu_kb)

@router.message(Search.by_style)
async def search_by_style_text_enter(msg:types.Message,state:FSMContext):
    if msg.text == bot_texts.back_btn:
        await msg.answer(bot_texts.back_str,reply_markup=kb.menu_kb)
        await state.clear()
        await search(msg)
    else:
        await state.clear()
        data = await db.fa_styles()
        names = []
        name_id = {}
        for i in data:
            name_id[i.name] = i.id
            names.append(i.name)
        res = await find_simular(names,msg.text,'style')
        if len(res)>0:
            books = [[i.id,i.name] for i in await db.fa_books_by_style(name_id[res[0][0]])]
            result = '\n'.join([f"/book_{i} | {j}" for i, j in books])
            result = (f'Вероятно вы имели ввиду жанр {res[0][0]}'
                      f'\nВот книги по данному запросу\n')+result
            text = bot_texts.search_find_str.replace('{{data}}', result)
            text_chunks = chunks(text, 4000)
            prev_msg_id = 0
            for i, chunk in enumerate(text_chunks):
                if i != 0:
                    chunk = bot_texts.text_chunk_start + chunk
                if i + 1 != len(text_chunks):
                    chunk = chunk + bot_texts.text_chunk_end
                if prev_msg_id != 0:
                    res = await msg.answer(chunk,
                                           reply_to_message_id=prev_msg_id,
                                           reply_markup=kb.menu_kb)
                else:
                    res = await msg.answer(chunk,reply_markup=kb.menu_kb)
                prev_msg_id = res.message_id
        else:
            await msg.answer(bot_texts.search_notfind_str,
                             reply_markup=kb.menu_kb)

async def find_simular(data,word,mode):
    if mode == 'style':
        limit = 1
    elif mode == 'author':
        limit = 1
    else:
        limit = 10
    data = process.extract(word,data,limit=limit)
    for value in data:
        if value[1] < config['search_percent']:
            data.remove(value)
    return data


@router.message(Style.add_enter_name)
async def style_add_handler(msg:types.Message,state:FSMContext):
    if msg.text == bot_texts.back_btn:
        await add_menu(msg,state)
    elif len(msg.text) > config['max_length_style']:
        await msg.answer(bot_texts.too_many_characters.replace('{{limit}}',
                        str(config['max_length_style'])),
                         reply_markup=await kb.back_or_menu_kb(back=True))
    else:
        style = name_formatter(msg.text)
        try:
            await db.insert_style(style)
            await msg.answer(
                bot_texts.add_style_good_str.replace('{{style}}', style))
        except sqlite3.IntegrityError:
            await msg.answer(
                bot_texts.error_unique.replace('{{value}}', style))
        except Exception as ex:
            print(f'[ADD EX] {ex}')
            await msg.answer(bot_texts.error_add)
        await menu(msg, state)


@router.message(F.text == bot_texts.add_author_btn)
async def add_author(msg:types.Message,state:FSMContext):
    await state.set_state(Author.add_enter_name)
    await msg.answer(bot_texts.add_author_str,
                     reply_markup=await kb.back_or_menu_kb(back=True))

@router.message(Author.add_enter_name)
async def author_add_handler(msg:types.Message,state:FSMContext):
    if msg.text == bot_texts.back_btn:
        await add_menu(msg,state)
    elif len(msg.text) > config['max_length_author']:
        await msg.answer(bot_texts.too_many_characters.replace('{{limit}}',
                        str(config['max_length_author'])),
                         reply_markup=await kb.back_or_menu_kb(back=True))
    else:
        author = name_formatter(msg.text)
        try:
            await db.insert_author(author)
            await msg.answer(
                bot_texts.add_author_good_str.replace('{{author}}', author))
        except sqlite3.IntegrityError:
            await msg.answer(
                bot_texts.error_unique.replace('{{value}}', author))
        except Exception as ex:
            print(f'[ADD EX] {ex}')
            await msg.answer(bot_texts.error_add)
        await menu(msg, state)


@router.message(Book.add_enter_name)
async def add_enter_name_handler(msg:types.Message,state:FSMContext):
    if msg.text == bot_texts.back_btn:
        await add_menu(msg,state)
    elif msg.text == bot_texts.back_btn:
        await add_menu(msg,state)
    elif len(msg.text) > config['max_length_book']:
        await msg.answer(bot_texts.too_many_characters.replace('{{limit}}',
                        str(config['max_length_book'])),
                         reply_markup=await kb.back_or_menu_kb(back=True))
    else:
        await state.update_data(book_name=msg.text)
        await state.set_state(Book.add_enter_author)
        data = await state.get_data()
        prev_data = f'Название {data["book_name"]}'
        await msg.answer(bot_texts.add_book_2_str\
                         .replace('{{prev_data}}',prev_data)
                         ,reply_markup=await kb.back_or_menu_kb(back=True))

@router.message(Book.add_enter_author)
async def add_enter_author_handler(msg:types.Message,state:FSMContext):
    if msg.text == bot_texts.back_btn:
        await state.set_state(Book.add_enter_name)
        await msg.answer(bot_texts.add_book_str,
                         reply_markup=await kb.back_or_menu_kb())
    else:
        if msg.text.isdigit():
            author = await db.select_author(msg.text)
            if author:
                await state.update_data(book_author=int(msg.text))
                data = await state.get_data()
                prev_data = (f'Название {data["book_name"]}'
                             f'\nАвтор {author.name}')
                await state.set_state(Book.add_enter_style)
                await msg.answer(bot_texts.add_book_3_str\
                                 .replace('{{prev_data}}',prev_data)
                                 ,reply_markup=await kb.back_or_menu_kb(back=True))
            else:
                await msg.answer(
                    bot_texts.invalid_id.replace('{{cmd}}', '/authors'))
        else:
            await msg.answer(bot_texts.invalid_id.replace('{{cmd}}','/authors'))

@router.message(Book.add_enter_style)
async def add_enter_style_handler(msg:types.Message,state:FSMContext):
    if msg.text == bot_texts.back_btn:
        await state.set_state(Book.add_enter_author)
        data = await state.get_data()
        prev_data = f'Название {data["book_name"]}'
        await msg.answer(bot_texts.add_book_2_str\
                         .replace('{{prev_data}}',prev_data),
                         reply_markup=await kb.back_or_menu_kb(back=True))
    else:
        if msg.text.isdigit():
            style = await db.get_style(int(msg.text))
            if style:
                data = await state.get_data()
                await db.insert_book(name=data['book_name'],
                                     author_id=data['book_author'],
                                     style_id=int(msg.text),data='')
                await state.clear()
                author = await db.get_author(data['book_author'])
                await msg.answer(bot_texts.add_book_final_str\
                                 .replace('{{name}}',data['book_name'])\
                                 .replace('{{author}}',author.name)\
                                 .replace('{{style}}',style.name))
                await menu(msg, state)
            else:
                await msg.answer(
                    bot_texts.invalid_id.replace('{{cmd}}', '/styles'))
        else:
            await msg.answer(bot_texts.invalid_id.replace('{{cmd}}','/styles'))

@router.message(filters.Command(commands='books'))
@router.message(F.text == bot_texts.show_books_btn)
async def show_books(msg:types.Message,state:FSMContext):
    books = await db.fa_books()
    data = '\n'.join([f"/book_{book.id} | {book.name}" for book in books])
    if len(data)>0:
        text = bot_texts.show_books_str.replace('{{data}}', data)
        text_chunks = chunks(text, 4000)
        prev_msg_id = 0
        for i, chunk in enumerate(text_chunks):
            if i != 0:
                chunk = bot_texts.text_chunk_start + chunk
            if i + 1 != len(text_chunks):
                chunk = chunk + bot_texts.text_chunk_end
            if prev_msg_id != 0:
                res = await msg.answer(chunk, reply_to_message_id=prev_msg_id)
            else:
                res = await msg.answer(chunk)
            prev_msg_id = res.message_id
    else:
        await msg.answer(bot_texts.show_books_empty_str)

@router.message(F.text.startswith('/book_'))
async def show_book(msg:types.Message):
    book = await db.get_book(msg.text[6:])
    if book is not None:
        style = await db.get_style(book.style_id)
        author = await db.get_author(book.author_id)
        await msg.answer(bot_texts.book_info_str \
                         .replace('{{name}}', book.name) \
                         .replace('{{author}}', str(author.name)) \
                         .replace('{{style}}', str(style.name)) \
                         .replace('{{data}}',str(book.data)),
                         reply_markup=await in_kb.book_kb(book.id))
    else:
        await msg.answer(bot_texts.book_not_found.replace("{{id}}",msg.text[6:]))

@router.message(F.text.startswith('/style_'))
async def show_style(msg:types.Message):
    style = await db.get_style(msg.text[7:])
    if style is not None:
        await msg.answer(bot_texts.style_info_str \
                         .replace('{{name}}', style.name),
                         reply_markup=await in_kb.style_kb(style.id))
    else:
        await msg.answer(bot_texts.style_not_found.replace("{{id}}",msg.text[7:]))

@router.message(F.text.startswith('/author_'))
async def show_author(msg:types.Message):
    author = await db.get_author(msg.text[8:])
    if author is not None:
        await msg.answer(bot_texts.author_info_str \
                         .replace('{{name}}', author.name),
                         reply_markup=await in_kb.author_kb(author.id))
    else:
        await msg.answer(bot_texts.author_not_found.replace("{{id}}",msg.text[8:]))

@router.callback_query(F.data.startswith('book_data:'))
async def book_data(call:types.CallbackQuery,state:FSMContext):
    await state.set_state(Book.enter_data)
    await state.update_data(book_id = call.data[10:])
    await call.message.delete()
    await call.message.answer(bot_texts.book_data_add,
                                 reply_markup=await kb.back_or_menu_kb(back=True))

@router.message(Book.enter_data)
async def book_data_enter(msg:types.Message,state:FSMContext):
    if msg.text == bot_texts.back_btn:
        data = await state.get_data()
        await state.clear()
        book = await db.get_book(data["book_id"])
        style = await db.get_style(book.style_id)
        author = await db.get_author(book.author_id)
        await msg.answer(bot_texts.book_info_str \
                         .replace('{{name}}', book.name) \
                         .replace('{{author}}', str(author.name)) \
                         .replace('{{style}}', str(style.name)) \
                         .replace('{{data}}', str(book.data)),
                         reply_markup=await in_kb.book_kb(book.id))
    else:
        data = await state.get_data()
        await state.clear()
        await db.update_book_data(data["book_id"],msg.text)
        await msg.answer(bot_texts.book_data_added,reply_markup=kb.menu_kb)
        book = await db.get_book(data["book_id"])
        style = await db.get_style(book.style_id)
        author = await db.get_author(book.author_id)
        await msg.answer(bot_texts.book_info_str \
                         .replace('{{name}}', book.name) \
                         .replace('{{author}}', str(author.name)) \
                         .replace('{{style}}', str(style.name)) \
                         .replace('{{data}}', str(book.data)),
                         reply_markup=await in_kb.book_kb(book.id))

@router.callback_query(F.data.startswith("book_edit_name:"))
async def book_edit_name(call:types.CallbackQuery,state:FSMContext):
    id = call.data[15:]
    await state.update_data(book_id=id)
    await state.set_state(Book.edit_name)
    await call.message.delete()
    await call.message.answer(bot_texts.edit_book_name_str,
                              reply_markup=await kb.back_or_menu_kb(back=True))

@router.message(Book.edit_name)
async def book_edit_name_enter(msg:types.Message,state:FSMContext):
    if msg.text == bot_texts.back_btn:
        data = await state.get_data()
        await state.clear()
        await msg.answer(bot_texts.back_str,reply_markup=kb.menu_kb)
        book = await db.get_book(data["book_id"])
        style = await db.get_style(book.style_id)
        author = await db.get_author(book.author_id)
        await msg.answer(bot_texts.book_info_str \
                         .replace('{{name}}', book.name) \
                         .replace('{{author}}', str(author.name)) \
                         .replace('{{style}}', str(style.name)) \
                         .replace('{{data}}', str(book.data)),
                         reply_markup=await in_kb.book_kb(book.id))
    else:
        data = await state.get_data()
        await db.update_book_name(data["book_id"],msg.text)
        await msg.answer(bot_texts.edit_book_name_success.replace('{{name}}',msg.text),
                         reply_markup=kb.menu_kb)
        await state.clear()
        book = await db.get_book(data["book_id"])
        style = await db.get_style(book.style_id)
        author = await db.get_author(book.author_id)
        await msg.answer(bot_texts.book_info_str \
                         .replace('{{name}}', book.name) \
                         .replace('{{author}}', str(author.name)) \
                         .replace('{{style}}', str(style.name)) \
                         .replace('{{data}}', str(book.data)),
                         reply_markup=await in_kb.book_kb(book.id))


@router.callback_query(F.data.startswith("book_edit_author:"))
async def book_edit_author(call:types.CallbackQuery,state:FSMContext):
    id = call.data[17:]
    await state.update_data(book_id=id)
    await state.set_state(Book.edit_author)
    await call.message.delete()
    await call.message.answer(bot_texts.edit_book_author_str,
                              reply_markup=await kb.back_or_menu_kb(back=True))

@router.message(Book.edit_author)
async def book_edit_author_enter(msg:types.Message,state:FSMContext):
    if msg.text == bot_texts.back_btn:
        data = await state.get_data()
        await state.clear()
        await msg.answer(bot_texts.back_str, reply_markup=kb.menu_kb)
        book = await db.get_book(data["book_id"])
        style = await db.get_style(book.style_id)
        author = await db.get_author(book.author_id)
        await msg.answer(bot_texts.book_info_str \
                         .replace('{{name}}', book.name) \
                         .replace('{{author}}', str(author.name)) \
                         .replace('{{style}}', str(style.name)) \
                         .replace('{{data}}', str(book.data)),
                         reply_markup=await in_kb.book_kb(book.id))
    elif await db.get_author(msg.text) is None:
        await msg.answer(bot_texts.author_not_found.replace("{{id}}",msg.text),
                         reply_markup=await kb.back_or_menu_kb(back=True))
    else:
        data = await state.get_data()
        await db.update_book_author_id(data["book_id"],msg.text)
        author = await db.get_author(msg.text)
        await msg.answer(bot_texts.edit_book_author_success.replace('{{name}}',author.name),
                         reply_markup=kb.menu_kb)
        await state.clear()
        book = await db.get_book(data["book_id"])
        style = await db.get_style(book.style_id)
        author = await db.get_author(book.author_id)
        await msg.answer(bot_texts.book_info_str \
                         .replace('{{name}}', book.name) \
                         .replace('{{author}}', str(author.name)) \
                         .replace('{{style}}', str(style.name)) \
                         .replace('{{data}}', str(book.data)),
                         reply_markup=await in_kb.book_kb(book.id))

@router.callback_query(F.data.startswith("book_edit_style:"))
async def book_edit_style(call:types.CallbackQuery,state:FSMContext):
    id = call.data[16:]
    await state.update_data(book_id=id)
    await state.set_state(Book.edit_style)
    await call.message.delete()
    await call.message.answer(bot_texts.edit_book_style_str,
                              reply_markup=await kb.back_or_menu_kb(back=True))

@router.message(Book.edit_style)
async def book_edit_style_enter(msg:types.Message,state:FSMContext):
    if msg.text == bot_texts.back_btn:
        data = await state.get_data()
        await state.clear()
        await msg.answer(bot_texts.back_str, reply_markup=kb.menu_kb)
        book = await db.get_book(data["book_id"])
        style = await db.get_style(book.style_id)
        author = await db.get_author(book.author_id)
        await msg.answer(bot_texts.book_info_str \
                         .replace('{{name}}', book.name) \
                         .replace('{{author}}', str(author.name)) \
                         .replace('{{style}}', str(style.name)) \
                         .replace('{{data}}', str(book.data)),
                         reply_markup=await in_kb.book_kb(book.id))
    elif await db.get_style(msg.text) is None:
        await msg.answer(bot_texts.style_not_found.replace("{{id}}",msg.text),
                         reply_markup=await kb.back_or_menu_kb(back=True))
    else:
        data = await state.get_data()
        await db.update_book_style_id(data["book_id"],msg.text)
        style = await db.get_style(msg.text)
        await msg.answer(bot_texts.edit_book_style_success.replace('{{name}}',style.name),
                         reply_markup=kb.menu_kb)
        await state.clear()
        book = await db.get_book(data["book_id"])
        style = await db.get_style(book.style_id)
        author = await db.get_author(book.author_id)
        await msg.answer(bot_texts.book_info_str \
                         .replace('{{name}}', book.name) \
                         .replace('{{author}}', str(author.name)) \
                         .replace('{{style}}', str(style.name)) \
                         .replace('{{data}}', str(book.data)),
                         reply_markup=await in_kb.book_kb(book.id))

@router.callback_query(F.data.startswith("style_edit_name:"))
async def style_edit_name(call:types.CallbackQuery,state:FSMContext):
    id = call.data[16:]
    await state.update_data(style_id=id)
    await state.set_state(Style.edit_name)
    await call.message.delete()
    await call.message.answer(bot_texts.edit_style_name_str,
                              reply_markup=await kb.back_or_menu_kb(back=True))

@router.message(Style.edit_name)
async def style_edit_name_enter(msg:types.Message,state:FSMContext):
    if msg.text == bot_texts.back_btn:
        data = await state.get_data()
        await state.clear()
        await msg.answer(bot_texts.back_str, reply_markup=kb.menu_kb)
        style = await db.get_style(data["style_id"])
        await msg.answer(bot_texts.style_info_str \
                         .replace('{{name}}', style.name),
                         reply_markup=await in_kb.style_kb(style.id))
    else:
        data = await state.get_data()
        await db.update_style_name(data["style_id"],msg.text)
        await msg.answer(bot_texts.edit_style_name_success.replace('{{name}}',msg.text),
                         reply_markup=kb.menu_kb)
        await state.clear()
        style = await db.get_style(data["style_id"])
        await msg.answer(bot_texts.style_info_str \
                         .replace('{{name}}', style.name),
                         reply_markup=await in_kb.style_kb(style.id))


@router.callback_query(F.data.startswith("author_edit_name:"))
async def author_edit_name(call:types.CallbackQuery,state:FSMContext):
    id = call.data[17:]
    print(id)
    await state.update_data(author_id=id)
    await state.set_state(Author.edit_name)
    await call.message.delete()
    await call.message.answer(bot_texts.edit_author_name_str,
                              reply_markup=await kb.back_or_menu_kb(back=True))

@router.message(Author.edit_name)
async def author_edit_name_enter(msg:types.Message,state:FSMContext):
    if msg.text == bot_texts.back_btn:
        data = await state.get_data()
        await state.clear()
        await msg.answer(bot_texts.back_str, reply_markup=kb.menu_kb)
        author = await db.get_author(data["author_id"])
        await msg.answer(bot_texts.author_info_str \
                         .replace('{{name}}', author.name),
                         reply_markup=await in_kb.author_kb(author.id))
    else:
        data = await state.get_data()
        await db.update_author_name(data["author_id"],msg.text)
        await msg.answer(bot_texts.edit_author_name_success.replace('{{name}}',msg.text),
                         reply_markup=kb.menu_kb)
        await state.clear()
        author = await db.get_author(data["author_id"])
        await msg.answer(bot_texts.author_info_str \
                         .replace('{{name}}', author.name),
                         reply_markup=await in_kb.author_kb(author.id))

@router.callback_query(F.data.startswith('book_delete:'))
async def book_delete(call:types.CallbackQuery):
    await db.delete_book(call.data[12:])
    await call.message.edit_text(bot_texts.book_delete_success)
    await call.message.answer(bot_texts.menu_str.replace('{{name}}',call.from_user.full_name),
                              reply_markup=kb.menu_kb)

@router.callback_query(F.data.startswith('style_delete:'))
async def style_delete(call:types.CallbackQuery):
    await db.delete_style(call.data[13:])
    await call.message.edit_text(bot_texts.style_delete_success)
    await call.message.answer(bot_texts.menu_str.replace('{{name}}',call.from_user.full_name),
                              reply_markup=kb.menu_kb)

@router.callback_query(F.data.startswith('author_delete:'))
async def author_delete(call:types.CallbackQuery):
    await db.delete_author(call.data[14:])
    await call.message.edit_text(bot_texts.author_delete_success)
    await call.message.answer(bot_texts.menu_str.replace('{{name}}',call.from_user.full_name),
                              reply_markup=kb.menu_kb)
menu_str = ("Добро пожаловать {{name}}"
        "\nвыберайте книгу на ваш вкус")

back_btn = "Назад"
menu_btn = "В меню"
search_btn = "Поиск"
to_add_kb_btn = 'Добавить книгу,автора,жанр'
to_add_kb_str = 'Что хотите добавить?'

search_methods_str = 'По какому параметру хотите искать?'

search_by_book_btn = 'Искать по названию книги'
search_by_author_btn = 'Искать по автору'
search_by_style_btn = 'Искать по жанру'

search_by_book_str = 'Введите название книги'
search_by_author_str = 'Введите название автора'
search_by_style_str = 'Введите название жанра'
search_find_str = 'По вашему запросу найдено следующее\n\n{{data}}'
search_notfind_str = 'По вашему запросу ничего не найдено('

add_book_btn = "Добавить книгу"
add_author_btn = 'Добавить автора'
add_style_btn = 'Добавить жанр'

show_books_btn = 'Книги'
show_authors_btn = 'Авторы'
show_styles_btn = 'Жанры'

show_styles_str = \
"""Вот /style_номер | название всех жанров
Хотите посмотреть/редактировать?
Просто нажмите на нужный жанр

{{data}}"""
show_authors_str = \
"""Вот /author_номер | название всех авторов
Хотите посмотреть/редактировать?
Просто нажмите на нужного автора

{{data}}"""
show_books_str = \
"""Вот /book_номер | название книг
Хотите посмотреть/редактировать?
Просто нажмите на нужную книгу

{{data}}"""

show_styles_empty_str = 'К сожалению жанров ещё нет'
show_authors_empty_str = 'К сожалению авторов ещё нет'
show_books_empty_str = 'К сожалению книг ещё нет'

add_book_str = "Хорошо введите название книги"
add_book_2_str = '{{prev_data}}\nВведите id автора\n/authors'
add_book_3_str = '{{prev_data}}\nВведите id жанра\n/styles'
add_book_final_str = """Книга успешно добавлена
Название: {{name}}
Автор: {{author}}
Жанр: {{style}}"""
add_author_str = 'Хорошо, введите автора'
add_style_str = 'Хорошо, введите жанр'

invalid_id = 'Данного id нету в списке\n{{cmd}}'

add_author_good_str = 'Автор {{author}} успешно добавлен'
add_style_good_str = 'Жанр {{style}} успешно добавлен'

error_add = 'Ошибка при добавлении'
error_unique = 'Значение {{value}} уже добавлено в базу данных'

book_info_str = """Книга
Название: {{name}}
Автор: {{author}}
Жанр: {{style}}
Данные: {{data}}"""

style_info_str = """Жанр
Название: {{name}}"""

author_info_str = """Автор
Название: {{name}}"""

book_not_found = "Книга с {{id}} ид не найдена"
style_not_found = "Жанр с {{id}} ид не найден"
author_not_found = "Автор с {{id}} ид не найден"

book_data_add = 'Укажите данные для книги(ссылка)'
book_data_added = 'Данные для книги добавлены'

add_book_data_btn = 'Добавить данные для книги'
delete_book_btn = 'Удалить книгу'
delete_author_btn = 'Удалить автора'
delete_style_btn = 'Удалить жанр'


edit_book_name_btn = 'Сменить имя'
edit_book_style_btn = 'Сменить жанр'
edit_book_author_btn = 'Сменить автора'
edit_style_name_btn = 'Сменить имя'
edit_author_name_btn = 'Сменить имя'

edit_book_name_str = 'Укажите новое имя для книги'
edit_book_style_str = 'Укажите новый id жанра для книги\n/styles'
edit_book_author_str = 'Укажите новый id автора для книги\n/authors'
edit_style_name_str = 'Укажите новое имя для жанра'
edit_author_name_str = 'Укажите новое имя для автора'

edit_book_name_success = 'Имя книги успешно изменено на {{name}}'
edit_book_style_success = 'Жанр книги успешно изменен на {{name}}'
edit_book_author_success = 'Автор книги успешно изменен на {{name}}'
edit_style_name_success = 'Имя жанра успешно изменено на {{name}}'
edit_author_name_success = 'Имя автора успешно изменено на {{name}}'

book_delete_success = 'Книга успешно удалена'
style_delete_success = 'Жанр успешно удален'
author_delete_success = 'Автор успешно удален'

back_str = "Возвращаем вас назад..."

too_many_characters = 'Слишком много символов, лимит у этого поля {{limit}}'

text_chunk_start = 'Это продолжение предыдущего сообщения\n\n'
text_chunk_end = '\n\nНе смогли всё уместить, продолжение ниже'
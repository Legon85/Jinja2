from jinja2 import FileSystemLoader, Environment

# При создании сайтов часто страницу делят на 3 части:
# header
# content
# footer

# То есть исходный шаблон страницы мы можем поделить на 3 части и каждую часть поместить в отдельный файл,
# а потом их соединить с помощью конструкции include.


# Разобьём страницу из нашего подкаталога htm на 3 составляющие:

# 1 часть:
# <!DOCTYPE html>
# <html>
# <head>
#     <meta charset="utf-8">
#     <base href="https://proproprogs.ru/">
#     <title>Про программирование</title>
# </head>


# 2 часть:
# <body>
#
# <u1>
# {% for u in users -%}
#     <li>{{u.name}}
# {% endfor -%}
# </u1>



# 3 часть:
# </body>
# </html>



# Создадим 3 вспомогательных файла соответственно:
# header.htm с содержанием:
# <!DOCTYPE html>
# <html>
# <head>
#     <meta charset="utf-8">
#     <base href="https://proproprogs.ru/">
#     <title>Про программирование</title>
# </head>


# footer.htm с содержанием:
# </body>
# </html>


# page.htm со следующим содержанием:
# {% include 'header.htm' %}
# <p>Содержание страницы
# {% include 'footer.htm' %}

# В основе файла page.htm будет абзац с текстом: Содержимое страницы, а всё остальное (header и footer)  в него будет
# как раз загружаться с помощью конструкции include.

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
tm = env.get_template('page.htm')
msg = tm.render()

print(msg)
print("-" * 60)
# На выходе получаем целостную страницу:
# <!DOCTYPE html>
# <html>
# <head>
#     <meta charset="utf-8">
#     <base href="https://proproprogs.ru/">
#     <title>Про программирование</title>
# </head>
# <p>Содержание страницы
# </body>
# </html>

# В случае если в конструкции include будет передан не существующий файл или прописан файл с ошибкой в названии
# вылетит исключение TemplateNotFound.
# Что бы избежать таких исключений в include дополнительно прописывается ignore missing:
# {% include 'header.htm' ignore missing %}
# <p>Содержание страницы
# {% include 'footer.htm' %}

# и в данном случае просто не будет загружено содержимое с проигнорированным файлом, а всё остальное загрузится:
# для проверки в файле page.htm изменить имя, например, файла header.htm
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
tm = env.get_template('page.htm')
msg = tm.render()

print(msg)
print("-" * 60)
# на выходе будет всё кроме контента из файла header.htm:
# <p>Содержание страницы
# </body>
# </html>

# В файле header.htm есть теги <base> со ссылкой на домен и <title> с названием заголовка. Предположим нам нужно
# чтобы мы туда могли подставлять любые нужные нам данные в нужный момент. Для этого надо в этом файле определить в
# этих местах вставку для шаблонов {{domain}} и {{title}}. А в параметрах метода render, где происходит обработка
# шаблона, передать два этих параметра domain и title.

# Для организации этих целей создадим отдельный файл header2.htm с описанным выше содержимым:
# <!DOCTYPE html>
# <html>
# <head>
#     <meta charset="utf-8">
#     <base href="{{domain}}">
#     <title>{{title}}</title>
# </head>

# В файле page.htm соответственно нужно в include поменять файл на header2.htm
# Загрузим наш файл с

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
tm = env.get_template('page.htm')
msg = tm.render(domain="https://proproprogs.ru/", title="Про jinja")

print(msg)
print("-" * 60)
# На выходе получим страницу с подставленными из render данными:
# <!DOCTYPE html>
# <html>
# <head>
#     <meta charset="utf-8">
#     <base href="https://proproprogs.ru/">
#     <title>Про jinja</title>
# </head>
# <p>Содержание страницы
# </body>
# </html>

# Если в блоке include нужно использовать сразу несколько страниц, то они просто перечисляются через запятую:
# {% include ['page1.htm', 'page2.htm'] ignore missing %}

# Кроме include есть ещё одна конструкция - import. Её отличие в том, что при импорте файл не добавляется,
# но мы можем использовать функционал этого файла. Часто это используется, когда в импортируемом файле находится
# какой-нибудь макрос и его мы уже используем в нашем исходном шаблоне.

# Для этого подготовим файл dialogs.htm в подкаталоге templates содержащий макрос:
# {% macro dialog_1(title, msg='') -%}
# <div class="dialog">
#     <p class="title">{{title}}</p>
#     <p class="message">{{msg}}</p>
#     <p><input type="button" value="Закрыть"></p>
# </div>
# {%- endmacro %}

# В макросе под названием dialog_1 передаются параметры title и msg.
# А далее тегами формируется диалоговое окно с полями title и message.

# Для демонстрации работы создадим отдельный файл page1.htm и импортируем туда макрос из выше описанного файла
# dialogs.htm, задав ему alias - dlg и прописав значения для макроса title- 'Внимание', message - 'Это тестовый диалог':

# {% import 'dialogs.htm' as dlg %}
# <p>Содержание страницы
# {{ dlg.dialog_1('Внимание', 'Это тестовый диалог') }}
# {% include 'footer.htm' %}

# Здесь мы импортируем dialogs.htm и далее формируем диалоговое окно, обращаясь через alias dlg к макросу dialog_1 -
# dlg.dialog_1('Внимание', 'Это тестовый диалог') и передавая ему параметры: 'Внимание', 'Это тестовый диалог'.

# Запустим и проверим что на выходе программы:
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
tm = env.get_template('page1.htm')
msg = tm.render(domain="https://proproprogs.ru/", title="Про jinja")

print(msg)
print("-" * 60)
# ->
# <p>Содержание страницы
# <div class="dialog">
#     <p class="title">Внимание</p>
#     <p class="message">Это тестовый диалог</p>
#     <p><input type="button" value="Закрыть"></p>
# </div>
# </body>
# </html>



# Так же импорты можно производить следующим образом:
# {% from 'dialogs.htm' import dialog_1 as dlg %}
# <p>Содержание страницы
# {{ dlg('Внимание', 'Это тестовый диалог') }}
# {% include 'footer.htm' %}

#  Вариант без alias'а
# {% from 'dialogs.htm' import dialog_1 %}
# <p>Содержание страницы
# {{ dialog_1('Внимание', 'Это тестовый диалог') }}
# {% include 'footer.htm' %}

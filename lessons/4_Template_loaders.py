from jinja2 import Environment, FileSystemLoader, FunctionLoader

# На предыдущих занятиях мы прописывали шаблоны в таком виде:
link = '''<select name="cities">  
{% for c in cities %}
    <option value="{{c['id']}}">{{c['city']}}</option>
{% endfor %}
</select>'''

# Но в действительности, как правило, они хранятся в отдельных текстовых файлах и загружаются по мере необходимости.
# Для реализации функционала такой загрузки шаблонов в jinja существует класс Environment.

# Предположим все наши шаблоны хранятся в отдельном подкаталоге templates относительно рабочего каталога
# lessons. И в подкаталоге templates есть файл main.htm содержащий следующий шаблон:
# <u1>
# {% for u in users -%}
#     <li>{{u.name}}
# {% endfor -%}
# </u1>

# Воспользуемся этим шаблоном (загрузим и обработаем его) для следующих данных:
persons = [{"name": "Aleksey", "old": 18, "weight": 78.5},
           {"name": "Nicolay", "old": 28, "weight": 82.3},
           {"name": "Ivan", "old": 33, "weight": 94.0}]

# Для загрузки шаблона нужно воспользоваться одним из загрузчиков jinja (FileSystemLoader), который в качестве
# параметра принимает подкаталог, из которого нужно загрузить шаблон(templates):
file_loader = FileSystemLoader('templates')
# далее мы создаём уже экземпляр класса Environment и ему в качестве именованного параметра loader передаём ссылку на
# наш загрузчик:
env = Environment(loader=file_loader)

# далее мы должны получить шаблон с которым будем работать (main.htm). Для этого вызываем метод get_template,
# который формирует экземпляр класса Template на основе содержимого файла main.htm
tm = env.get_template('main.htm')
# и уже далее у экземпляра класса Template (tm) будем вызывать знакомый нам метод render.
msg = tm.render(users=persons)

# На выходе получаем содержимое файла main.htm и обработанный шаблоном в этом файле список persons.
print(msg)
print("-" * 60)

# ->
#         <!DOCTYPE html>
#         <html>
#         <head>
#             <meta charset="utf-8">
#             <base href="https://proproprogs.ru/">
#             <title>Про программирование</title>
#         </head>
#         <body>
#
#         <u1>
#         <li>Aleksey
#         <li>Nicolay
#         <li>Ivan
#         </u1>
#
#         </body>
#         </html>

# Для корректной работы такие файлы - шаблоны (main.htm) необходимо сохранять в формате utf-8.

# Список стандартных загрузчиков jinja следующий:

# templates:
# PackageLoader - для загрузки шаблонов из пакета;
# DictLoader - для загрузки шаблонов из словаря;
# FunctionLoader - для загрузки на основе функции;
# PrefixLoader - загрузчик, использующий словарь для построения по, каталогов;
# ChoiceLoader - загрузчик, содержащий список других загрузчиков (если один не сработает, выбирается следующий);
# ModuleLoader - загрузчик для скомпилированных шаблонов.

# В качестве примера рассмотрим ещё как работает загрузчик FunctionLoader.
# По сути он работает на основе некой функции. Поэтому напишем эту функцию:

persons = [{"name": "Aleksey", "old": 18, "weight": 78.5},
           {"name": "Nicolay", "old": 28, "weight": 82.3},
           {"name": "Ivan", "old": 33, "weight": 94.0}]


def loadTpl(path):
    if path == 'index':                                     # если функции передаётся 'index', то...
        return '''Имя {{u.name}}, возраст {{u.old}}'''      # возвращаем имя и возраст
    else:
        return '''Данные: {{u}}'''                          # в противном случае возвращаем весь словарь с данными


file_loader = FunctionLoader(loadTpl)           # В данном случае передаётся именно ссылка на функцию, т.е. без скобок.
env = Environment(loader=file_loader)

tm = env.get_template('index')
msg = tm.render(u=persons[0])

# из коллекции persons берётся только первое значение, потому что шаблон в функции
# отображает только одно конкретное значение и вместо users - u, потому что так же в шаблоне используется  u.

print(msg)

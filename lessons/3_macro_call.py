from jinja2 import Template
# Рассмотрим фильтры которые удобно применять для получения более сложных представлений.


# sum - вычисление суммы поля коллекции:

# Предположим, имеется такой список автомобилей и требуется вывести суммарную цену для всех автомобилей:

cars = [
    {'model': 'Audi', 'price': 23000},
    {'model': 'Scoda', 'price': 17300},
    {'model': 'Volvo', 'price': 44300},
    {'model': 'Volksvagen', 'price': 21300}
]

tpl = "Суммарная цена автомобилей {{ cs | sum(attribute='price') }}"
tm = Template(tpl)
msg = tm.render(cs=cars)

# в данном шаблоне указывается для какой коллекции будет вызываться фильтр, далее вертикальная черта и сам фильтр sum
# с указанием по какому полю будет суммироваться ('price')
print(msg)  # - > Суммарная цена автомобилей 105900
print('-' * 60)

# В общем случае синтаксис фильтра sum следующий:
# sum(iterable, attribute=None, start=o) Где start - прибавка к вычисленной сумме, если это необходимо.
# Таких фильтров в jinja много: abs(), attr(), float(), lower()...... более подробно в документации jinja.

# Например, для выведения максимально цены используется фильтр max:

tpl = "Максимальная цена автомобиля {{ cs | max(attribute='price') }}"
tm = Template(tpl)
msg = tm.render(cs=cars)

print(msg)  # -> Максимальная цена автомобиля {'model': 'Volvo', 'price': 44300}
print('-' * 60)

# Если же необходимо вывести лишь марку автомобиля с максимальной ценой, то нужно всю конструкцию внутри шаблона взять
# скобки, как бы обращаясь ко всему словарю {'model': 'Volvo', 'price': 44300} и через точку прописать ключ 'model'
# который вернёт нам марку:

tpl = "Максимальная цена у автомобиля {{ (cs | max(attribute='price')).model }}"
tm = Template(tpl)
msg = tm.render(cs=cars)

print(msg)
print('-' * 60)
#  ->  Максимальная цена у автомобиля Volvo

# то же самое с фильтром min:

tpl = "Минимальная цена у автомобиля {{ (cs | min(attribute='price')).model }}"
tm = Template(tpl)
msg = tm.render(cs=cars)

print(msg)
print('-' * 60)
# - > Минимальная цена у автомобиля Scoda

# фильтр random позволяет случайным образом получить запись из коллекции:

tpl = "Автомобиль: {{ cs | random }}"
tm = Template(tpl)
msg = tm.render(cs=cars)

print(msg)
print('-' * 60)
# -> Автомобиль: {'model': 'Scoda', 'price': 17300}

# фильтр для замены малых букв о, на заглавные О:

tpl = "Автомобиль: {{ cs | replace('o', 'O')}}"
tm = Template(tpl)
msg = tm.render(cs=cars)

print(msg)
print('-' * 60)
# - > Автомобиль: [{'mOdel': 'Audi', 'price': 23000}, {'mOdel': 'ScOda', 'price': 17300},
# {'mOdel': 'VOlvO', 'price': 44300}, {'mOdel': 'VOlksvagen', 'price': 21300}]

# Фильтры так же можно применять и внутри шаблонов:
# {{% filter<название фильтра>%}}
# <фрагмент для применения фильтра>
# {% endfilter %}

# Например, есть список persons:

с

tpl = '''
{% for u in users -%}
{% filter upper %}{{u.name}}{% endfilter%}
{% endfor -%}'''

# перебираем список с помощью ранее изученного блока {% for u in users -%}
# Далее к каждому имени этого списка {{u.name}}
# применяем фильтр upper {% filter upper %}

tm = Template(tpl)
msg = tm.render(users=persons)

print(msg)
print('-' * 60)
# - >
#         ALEKSEY
#         NICOLAY
#         IVAN

# Модуль jinja поддерживает макроопределения для шаблонов, которые весьма полезны, чтобы избежать повторяемых
# определений в соответствии с принципом  DRY - don't repeat yourself(не повторяйся).

# Предположим мы формируем html документ и хотим создать несколько полей input. Для этого прописывается следующее
# макроопределение:

html = '''
{% macro input(name, value='', type='text', size=20) -%}
    <input type="{{ type }}" name="{{ name }}" value="{{ value | e }}" size="{{ size }}">
{%- endmacro %}

<p>{{ input('username') }}
<p>{{ input('email') }}
<p>{{ input('password') }}
'''
# В шаблоне {%-%} прописывается ключевое слово macro и его имя input, а так же набор параметров если они необходимы:
# name, value='', type='text', size=20 - все кроме name это параметры по умолчанию.
# далее в теге <input> все элементы name, value, type, size принимают соответствующие значения из выше
# обозначенного блока, при чём к value дополнительно применяется флаг экранирования e.
# Далее формируем шаблон, в котором можем использовать макрос множество раз.
# В теге абзаца <p> формируем тег <input> из макроса. И указываем что поле 'name' из макроса будет принимать
# значение
# 'username', а остальные параметры возьмём по умолчанию.
# То же самое для следующего поля ввода: здесь у него 'name' будет принимать значение 'email'.
# И далее аналогично: 'name' будет принимать значение 'password'.
# Далее создаём этот шаблон и обрабатываем его.
tm = Template(html)
msg = tm.render()

print(msg)
print('-' * 60)
# - >
#         <p><imput type="text" name="username" value="" size="20">
#         <p><imput type="text" name="email" value="" size="20">
#         <p><imput type="text" name="password" value="" size="20">


# Jinja имеет определение call, которое позволяет создавать вложенные макросы:
# {% call[(параметры)]<вызов макроса>%}
# <вложенный шаблон>
# {% endcall %}

# Предположим нужно создать html со списком людей, при этом каждый человек будет содержать в себе ещё один список с
# данными о себе (age, weight) следующего вида:
# <ul>
# <li>Aleksey
#     <ul>
#     <li>age:
#     <li>weight: 78.5
#     </ul>
# <li>Nicolay
#     <ul>
#     <li>age:
#     <li>weight:82.3
#     </ul>
# <Ivan>
#     <ul>
#     <li>age:
#     <li>weight:94.0
#     </ul>
# </ul>

# Создадим список persons, который будет хранить всю эту информацию:

persons = [{"name": "Aleksey", "old": 18, "weight": 78.5},
           {"name": "Nicolay", "old": 28, "weight": 82.3},
           {"name": "Ivan", "old": 33, "weight": 94.0}]

# Пропишем макроопределение, которое будет создавать главный список из имён людей:

html = '''
{% macro list_users(list_of_users) -%}
<ul>
{% for u in list_of_users -%}
    <li>{{u.name}}
{%- endfor %}
</ul>
{%- endmacro%}

{{list_users(users)}}
'''

# Здесь мы формируем макроопределение с названием list_users и мы ему передаём некий список list_of_users.
# Внутри этого макроопределения формируем список <ul></ul>, в котором будут формироваться теги <li> с именами
# людей из списка, посредством перебора элементов списка list_of_users в блоке {% for %}
#
# Далее вызываем это макроопределение с параметром users: {{list_users(users)}},
# который берется из метода render(см.далее...)
#
# Когда мы будем выполнять написанный шаблон, то список persons определённый в методе render будет передаваться в шаблон
# и далее он подставится в макрос в list_of_users. То есть в list_of_users будет ссылка на persons.
# Далее мы этот список перебираем и формируем из него теги <li>
#
tm = Template(html)
msg = tm.render(users=persons)

print(msg)
print('-' * 60)
# ->
#         <ul>
#         <li>Aleksey<li>Nicolay<li>Ivan
#         </ul>

# Теперь для этого списка добавим ещё вложенные списки с помощью блока {% call%}:
#     <ul>
#     <li>age:
#     <li>weight: 78.5
#     </ul>

#     <ul>
#     <li>age:
#     <li>weight:82.3
#     </ul>

# и...

#     <ul>
#     <li>age:
#     <li>weight:94.0
#     </ul>

html = '''
{% macro list_users(list_of_users) -%}
<ul>
{% for u in list_of_users -%}
    <li>{{u.name}} {{caller(u)}}
{%- endfor %}
</ul>
{%- endmacro %}

{% call(user) list_users(users) %}
    <ul>
    <li>age: {{user.old}}
    <li>weight: {{user.weight}}
    </ul>
{% endcall -%}
'''

# В данном случае в макросе, который уже был написан, при переборе имён в блоке {% for %}, в теге <li> будет вставлен
# блок метода {{ caller }}, который определён ниже по документу. Этот метод вызывается от u {{ caller(u)}}, то есть от
# каждого элемента в перебираемом блоке {% for %}. Таким образом он будет применён к каждому элементу в переборе.
#
# Макрос list_users(user) в методе {% call(user) list_users(user) %} это как бы связка блока {call} с макросом внешнего
# списка - {% macro list_users(list_of_users) -%}.
# Кроме того здесь макрос list_users выполняется с параметром (users), то есть со списком persons.
#
# Далее этот макрос начинает отрабатывать и, когда встречается функция {{ caller(u)}}, то соответственно вместо неё
# вставляется то, что идёт внутри блока {% call %}
#
# Ну и на выходе получаем:

tm = Template(html)
msg = tm.render(users=persons)

print(msg)
print('-' * 60)
# - >
#         <ul>
#         <li>Aleksey
#             <ul>
#             <li>age: 18
#             <li>weight: 78.5
#             </ul>
#         <li>Nicolay
#             <ul>
#             <li>age: 28
#             <li>weight: 82.3
#             </ul>
#         <li>Ivan
#             <ul>
#             <li>age: 33
#             <li>weight: 94.0
#             </ul>
#
#         </ul>

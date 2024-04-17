from jinja2 import Template
from markupsafe import escape

# Рассмотрим способы экранирования данных в строках.
# Допустим мы бы не хотели никак преобразовывать фрагмент шаблона {{name}} в следующей строчке:

data = '''Модуль jinja вместо 
определения {{name}}
подставляет соответствующее значение'''

tm = Template(data)
msg = tm.render(name='Федор')

print(msg, '\n', '-' * 60)

# Для этого в jinja есть специальный блок {%raw%}...{%endraw%}:

data = '''{%raw%}Модуль jinja вместо 
определения {{name}}
подставляет соответствующее значение{%endraw%}'''

tm = Template(data)
msg = tm.render(name='Федор')

print(msg, '\n', '-' * 60)  # - >

# Модуль jinja вместо
# определения {{name}}
# подставляет соответствующее значение

# При работе с текстовыми html шаблонами часто возникает необходимость экранировать символы, которые браузером
# воспринимаются как определения тегов. Например:

link = '''В HTML-документе ссылки определяются так:
<a href="#">Ссылка</a>'''

# если эту ссылку провести через метод render то, в принципе, она так и выведется:

tm = Template(link)
msg = tm.render()
print(msg, '\n', '-' * 60)  # ->
# В HTML-документе ссылки определяются так:
# <a href="#">Ссылка</a>

# Но! Если этот текст сохранить в виде html-файла (см. ex.html) и запустить в браузере, то всё, что находится в скобках(
# тег) отобразится в виде ссылки - Ссылка.

# Для того чтобы этот текст(<a href="#">Ссылка</a>) выводился в таком же виде и в браузере в jinja существует флаг e.
# И используется следующий синтаксис:
link = '''В HTML-документе ссылки определяются так:
<a href="#">Ссылка</a>'''

tm = Template("{{link | e }}")
msg = tm.render(link=link)
print(msg, '\n', '-' * 60)  # ->
# В HTML-документе ссылки определяются так:
# &lt;a href=&#34;#&#34;&gt;Ссылка&lt;/a&gt;

# Теперь если такой текст, выводимый в программе сохранить в html-документе(см. ex2.html), то при его открытии в
# браузере отобразиться исходный текст:
# В HTML-документе ссылки определяются так:
# <a href="#">Ссылка</a>

# Но в принципе можно записать всё вышеописанное, ИМПОРТИРОВАВ МОДУЛЬ escape из jinja, так же следующим синтаксисом:
link = '''В HTML-документе ссылки определяются так:
<a href="#">Ссылка</a>'''

msg = escape(link)
print(msg, '\n', '-' * 60)  # ->
# В HTML-документе ссылки определяются так:
# &lt;a href=&#34;#&#34;&gt;Ссылка&lt;/a&gt;

# НО! В ПОСЛЕДНИХ ВЕРСИЯХ JINJA БЫЛ УДАЛЁН   ESCAPE! и импортируется он не из jinja а следующим образом:
# from markupsafe import escape

# Так же можно использовать блок:
# {%for<выражение>-%}
#     <повторяемый фрагмент>
# {%endfor%}

cities = [{'id': 1, 'city': 'Moscow'},
          {'id': 5, 'city': 'Tver'},
          {'id': 7, 'city': 'Minsk'},
          {'id': 8, 'city': 'Smolensk'},
          {'id': 11, 'city': 'Kaluga'}]

# С помощью блока for сформировать в html документе (см. cities.html) строчки выпадающего списка из выше
# представленного списка.

link = '''<select name="cities">  
{% for c in cities %}
    <option value="{{c['id']}}">{{c['city']}}</option>
{% endfor %}
</select>'''

tm = Template(link)
msg = tm.render(cities=cities)

# В данном случае на каждой итерации цикла берутся данные для шаблона из списка cities (id и city)

print(msg, '\n', '-' * 60)

# Для того чтоб в выводе программы между строками html кода не было пустых строк нужно перед строками перед которыми
# есть перенос строки бок for закрывать со знаком '-' :   {% for -%}

link = '''<select name="cities">  
{% for c in cities -%}
    <option value="{{c['id']}}">{{c['city']}}</option>
{% endfor -%}
</select>'''

tm = Template(link)
msg = tm.render(cities=cities)

print(msg, '\n', '-' * 60)  # - >
# </select>
# <select name="cities">
# <option value="1">Moscow</option>
# <option value="5">Tver</option>
# <option value="7">Minsk</option>
# <option value="8">Smolensk</option>
# <option value="11">Kaluga</option>
# </select>

# Так же есть блок {% if<условие> %}:
# {% if<условие> %}
#   <фрагмент при истинности условия
# {% endif %}
#
# Можно использовать его в блоке for прошлого примера и добавлять в цикле строчки с городами только если id будет
# больше 6, например. (см. cities_if.html)
#
link = '''<select name="cities">  
{% for c in cities -%}
{%if c.id > 6 -%}
    <option value="{{c['id']}}">{{c['city']}}</option>
{% endif -%}
{% endfor -%}
</select>'''

tm = Template(link)
msg = tm.render(cities=cities)

print(msg, '\n', '-' * 60)  # теперь появились только те города, у которых id > 6. ->
# <select name="cities">
# <option value="7">Minsk</option>
# <option value="8">Smolensk</option>
# <option value="11">Kaluga</option>
# </select>

# Добавим условие else в наш код. И по нему будет просто прописан город без тега <option>
link = '''<select name="cities">  
{% for c in cities -%}
{%if c.id > 6 -%}
    <option value="{{c['id']}}">{{c['city']}}</option>
{% else -%}
    {{c['city']}}
{% endif -%}
{% endfor -%}
</select>'''

tm = Template(link)
msg = tm.render(cities=cities)

print(msg, '\n', '-' * 60)  # ->
# <select name="cities">
# Moscow
# Tver
# <option value="7">Minsk</option>
# <option value="8">Smolensk</option>
# <option value="11">Kaluga</option>
# </select>


# Добавим elif: (cities_if_elif_else.html)

link = '''<select name="cities">  
{% for c in cities -%}
{%if c.id > 6 -%}
    <option value="{{c['id']}}">{{c['city']}}</option>
{% elif c.city == "Moscow" -%}
    <option>{{c['city']}}</option>
{% else -%}
    {{c['city']}}
{% endif -%}
{% endfor -%}
</select>'''

tm = Template(link)
msg = tm.render(cities=cities)

print(msg, '\n', '-' * 60)  # ->
# <select name="cities">
# <option>Moscow</option>
# Tver
# <option value="7">Minsk</option>
# <option value="8">Smolensk</option>
# <option value="11">Kaluga</option>
# </select>

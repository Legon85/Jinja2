# На основе базового шаблона ex_main.htm написать в дочернем шаблоне about.htm расширение block title
# содержимым: О сайте  и  block content содержимым:
# <h1>О сайте</h1>
# <p>Классный сайт, если его доделать.</p>

# Вывести содержимое.

# Сделать расширение на основе базового шаблона default.tpl из подкаталога layout.
# Вывести результат.

# Поскольку в блоке block title и блоке block content есть часть данных в тегах, представляющая собой одинаковое
# содержимое, определить в блоке block content вызов дублируемых данных из блока block title.

# В базовом шаблоне default.tpl в блоке block content прописать следующее содержимое: Блок контента и сделать
# так, чтобы оно отображалось после расширения дочерним шаблоном. Вывести результат.

# Добавить в базовый шаблон в block content вложенный блок:
#         {% block table_contents %}
#         <ul>
#         {% for li in list_table -%}
#         <li>{{li}}</li>
#         {% endfor -%}
#         </ul>
#         {% endblock table_contents %}

# Для наполнения блока данными использовать список:
# subs = ['Математика', 'Физика', 'Информатика', 'Русский'] подаваемый на вход render.
# Сделать так, чтобы эти данные из базового шаблона выводились после расширения. Вывести результат.


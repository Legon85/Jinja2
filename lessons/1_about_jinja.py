from jinja2 import Template

name = "Федор"

tm = Template("Привет {{name}}")  # создаём экземпляр класса Template из модуля Jinja
msg = tm.render(name=name)  # вызываем метод render передавая ему ссылку из шаблона {{name}} на глобальную переменную
# name

print(msg)  # в результате получаем готовый обработанный шаблон:  Привет Федор

# Так же в шаблонах можно писать следующие конструкции:
# {%%} - спецификатор шаблона.
# {{ }} - выражение для вставки конструкций Python в шаблон.
# {##} - блок комментариев.
# # ## - строковый комментарий.
#
# Добавим к прошлому примеру ещё шаблонов

name = "Федор"
age = 28

tm = Template("Мне {{a}} лет и зовут {{n}}")
msg = tm.render(n=name, a=age)
print(msg)  # -> Мне 28 лет и зовут Федор
# То есть метод render принимает словари ключ:значение и значения подставляются в шаблон.

# Внутри конструкции {{}} можно прописывать любые Python конструкции и выражения. Например, можно сделать так:
tm = Template("Мне {{a*2}} лет и зовут {{n.upper()}}")
msg = tm.render(n=name, a=age)
print(msg)  # -> Мне 56 лет и зовут ФЕДОР


# Можно, например, вывести значения имени и возраста из свойств объекта класса:

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


per = Person('Федор', 33)


tm = Template("Мне {{p.age}} лет и зовут {{p.name}}")
msg = tm.render(p=per)
print(msg)  # -> Мне 33 лет и зовут Федор

# когда мы что-либо передаём в методе render (p=per), то это доступно внутри шаблона{{p.age}} по этой ссылке (p)


# Можно внутри класса прописать методы get_name   get_age  и получать имя и возраст в шаблонах через них:
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_name(self):
        return self.name

    def get_age(self):
        return self.age


per = Person('Федор', 33)


tm = Template("Мне {{p.get_age()}} лет и зовут {{p.get_name()}}")
msg = tm.render(p=per)
print(msg)  # -> Мне 33 лет и зовут Федор

# Так же можно передать данные в шаблон непосредственно с помощью словаря:

per = {'name': 'Федор', 'age': 34}

tm = Template("Мне {{p.age}} лет и зовут {{p.name}}")
msg = tm.render(p=per)
print(msg)  # -> Мне 34 лет и зовут Федор

# Ну или таким образом:
tm = Template("Мне {{p['age']}} лет и зовут {{p['name']}}")  # другой вариант обращения к значениям словаря
msg = tm.render(p=per)
print(msg)  # -> Мне 34 лет и зовут Федор


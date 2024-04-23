<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{% block title %}{% endblock %}</title>
</head>
<body>

{% block content %}
        {% block table_contents %}
        <ul>
        {% for li in list_table -%}
        <li>{% block item scoped %}{{ li }}{% endblock %}</li>
        {% endfor -%}
        </ul>
        {% endblock table_contents %}

{% endblock content %}

</body>
</html>
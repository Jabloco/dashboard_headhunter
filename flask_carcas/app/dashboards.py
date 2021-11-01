from io import BytesIO
import base64

import matplotlib.pyplot as plt

from constants import labels


def dash_link(figure):
    """
    Создает ссылку на изображение для вставки в шаблон html.

    Аргументы:
        figure - объект фигуры.
    """

    # Save it to a temporary buffer.
    buf = BytesIO()
    figure.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f'data:image/png;base64,{data}'


def create_pie_dashboard(levels_count: dict):
    """
    Функция принимает словарь вида {'junior': count, 'middle': count, 'senior': count}
    """

    # добавил проверку ключей во входящем словаре и сравнением с контстантой labels
    # иначе если количество ключей не совпадает с labels то падает с ошибкой
    sizes = [levels_count[label.upper()] for label in labels if label.upper() in levels_count]
    labels_name = [label for label in labels if label.upper() in levels_count]

    figure, ax = plt.subplots()
    ax.pie(
        sizes,
        labels=labels_name,
        autopct=lambda p: '{:.0f}'.format(p * sum(sizes) / 100),  # счетчик вместо процентов
        shadow=True,
        startangle=90
    )

    return figure


def create_keyskills_dashboard(keyskills_count: dict):
    names = list(keyskills_count.keys())
    values = list(keyskills_count.values())

    figure, ax = plt.subplots()
    ax.bar(names, values)
    ax.set_ylabel('Количество упоминаний')
    plt.subplots_adjust(bottom=0.3)  # увеличинени нижнего поля под графиком
    plt.xticks(rotation=30, ha='right', va='top', fontsize='small')  # наклон меток и размер шрифта

    return figure

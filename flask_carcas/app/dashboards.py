from io import BytesIO
import base64

import matplotlib.pyplot as plt

from constants import labels


def dash_link(figure):
    """
    Создает ссылку на изображение для вставки в шаблон html.

    Аргументы:
        figure - функция создания диаграммы.
    """
    fig = figure
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f'data:image/png;base64,{data}'

def create_pie_dashboard(levels_count: dict):
    """
    Функция принимает словарь вида {'junior': count, 'middle': count, 'senior': count}
    """

    sizes = [levels_count[label.upper()] for label in labels]

    figure, ax = plt.subplots()
    ax.pie(
        sizes,
        labels=labels,
        autopct=lambda p: '{:.0f}'.format(p * sum(sizes) / 100),  # счетчик вместо процентов
        shadow=True,
        startangle=90
    )

    return figure

import matplotlib.pyplot as plt
from io import BytesIO
import base64


def dash_link(create_dashboard):
    """
    Создает ссылку на изображение для вставки в шаблон html.

    Аргументы:
        create_dashboard - функция создания диаграммы.
    """
    fig = create_dashboard()
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
    labels = 'junior', 'middle', 'senior'
    sizes = [levels_count[label] for label in labels]

    figure, ax = plt.subplots()
    ax.pie(
        sizes,
        labels=labels,
        autopct=lambda p: '{:.0f}'.format(p * sum(sizes) / 100),  # счетчик вместо процентов
        shadow=True,
        startangle=90
    )

    return figure

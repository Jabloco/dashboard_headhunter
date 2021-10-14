import matplotlib.pyplot as plt
from io import BytesIO
import base64

def pie_chart(levels_count: dict):
    """
    Функция принимает словарь вида {'junior': count, 'middle': count, 'senior': count}
    """
    labels = 'junior', 'middle', 'senior'
    sizes = [levels_count['junior'], levels_count['middle'], levels_count['senior']]

    fig, ax = plt.subplots()
    ax.pie(
        sizes, labels=labels, 
        autopct=lambda p: '{:.0f}'.format(p * sum(sizes) / 100),
        shadow=True,
        startangle=90
    )
   
    return fig


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

if __name__ == '__main__':
    level = {'junior': 12, 'middle': 5, 'senior': 3}
    print(pie_chart(level))
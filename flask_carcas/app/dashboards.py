import matplotlib.pyplot as plt


def pie_dashboard(levels_count: dict):
    """
    Функция принимает словарь вида {'junior': count, 'middle': count, 'senior': count}
    """
    labels = 'junior', 'middle', 'senior'
    sizes = [levels_count['junior'], levels_count['middle'], levels_count['senior']]

    figure, ax = plt.subplots()
    ax.pie(
        sizes,
        labels=labels,
        autopct=lambda p: '{:.0f}'.format(p * sum(sizes) / 100),  # счетчик вместо процентов
        shadow=True,
        startangle=90
    )

    return figure

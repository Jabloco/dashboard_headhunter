import matplotlib.pyplot as plt


def pie_dashboard(levels_count: dict):
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

def salary_dashboard():
    """
    Создает график по ЗП.
    """
    

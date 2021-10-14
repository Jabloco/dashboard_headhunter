from pathlib import Path
import matplotlib.pyplot as plt

def pie_chart(levels_count: dict):
    """
    Функция принимает словарь вида {'junior': count, 'middle': count, 'senior': count}
    """
    labels = 'junior', 'middle', 'senior'
    sizes = [levels_count['junior'], levels_count['middle'], levels_count['senior']]

    dir_path = Path.cwd()
    path = Path(dir_path, 'charts', 'pie_chart.png')

    fig1, ax1 = plt.subplots()
    ax1.pie(
        sizes, labels=labels, 
        autopct=lambda p: '{:.0f}'.format(p * sum(sizes) / 100),
        shadow=True,
        startangle=90
    )
    # ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # os.chmod(fname, 0o400)
    print(path)
    return(plt.savefig(path, format='png'))
    
    return(plt.show())

if __name__ == '__main__':
    level = {'junior': 12, 'middle': 5, 'senior': 3}
    pie_chart(level)
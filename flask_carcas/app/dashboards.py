from matplotlib.figure import Figure
from io import BytesIO
import base64

def dash_link(create_dashboard):
    """"""
    fig = create_dashboard()
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f'data:image/png;base64,{data}'

def create_pie_dashboard():
    """Создает диаграмму."""
    fig = Figure()
    ax = fig.subplots()
    ax.pie([50, 30, 20])
    return fig

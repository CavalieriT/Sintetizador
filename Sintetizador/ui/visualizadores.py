import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MultipleLocator

def crear_visualizadores(parent):
    """
    Crea los tres gráficos de visualización de ondas.
    Retorna (fig1, ax1, canvas1, fig2, ax2, canvas2, fig3, ax3, canvas3).
    """
    fig1, ax1 = plt.subplots(figsize=(5, 2))
    ax1.set_title("Oscilador 1", fontsize=14, fontweight='bold', pad=10)
    ax1.set_xlabel("Tiempo (s)", fontsize=9)
    ax1.set_ylabel("Amplitud", fontsize=9)
    ax1.xaxis.set_major_locator(MultipleLocator(0.002))
    fig1.subplots_adjust(bottom=0.18, top=0.85)
    canvas1 = FigureCanvasTkAgg(fig1, master=parent)
    w1 = canvas1.get_tk_widget()
    w1.place(x=450, y=20, width=350, height=180)
    canvas1.draw()

    fig2, ax2 = plt.subplots(figsize=(5, 2))
    ax2.set_title("Oscilador 2", fontsize=14, fontweight='bold', pad=10)
    ax2.set_xlabel("Tiempo (s)", fontsize=9)
    ax2.set_ylabel("Amplitud", fontsize=9)
    ax2.xaxis.set_major_locator(MultipleLocator(0.002))
    fig2.subplots_adjust(bottom=0.18, top=0.85)
    canvas2 = FigureCanvasTkAgg(fig2, master=parent)
    w2 = canvas2.get_tk_widget()
    w2.place(x=450, y=220, width=350, height=180)
    canvas2.draw()

    fig3, ax3 = plt.subplots(figsize=(5, 2))
    ax3.set_title("Onda Combinada", fontsize=14, fontweight='bold', pad=10)
    ax3.set_xlabel("Tiempo (s)", fontsize=9)
    ax3.set_ylabel("Amplitud", fontsize=9)
    ax3.xaxis.set_major_locator(MultipleLocator(0.002))
    fig3.subplots_adjust(bottom=0.18, top=0.85)
    canvas3 = FigureCanvasTkAgg(fig3, master=parent)
    w3 = canvas3.get_tk_widget()
    w3.place(x=820, y=20, width=390, height=380)
    canvas3.draw()

    return fig1, ax1, canvas1, fig2, ax2, canvas2, fig3, ax3, canvas3
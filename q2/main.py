
import os
import numpy as np

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from about_window import AboutWindow    



class IceCreamWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.temperatures = []
        self.revenues = []

        self.about_window = AboutWindow()    
        self.initUI()


    def initUI(self):
        self.setWindowTitle("Ice Cream Revenue vs Temperature")
        self.resize(900, 650)

        layout = QVBoxLayout()

        buttons = QHBoxLayout()
        self.load_button = QPushButton("Load CSV File")
        self.load_button.clicked.connect(self.load_file)
        self.about_button = QPushButton("About")
        self.about_button.clicked.connect(self.show_about)
        buttons.addWidget(self.load_button)
        buttons.addStretch()
        buttons.addWidget(self.about_button)
        layout.addLayout(buttons)

        self.figure = Figure(figsize=(8, 5))
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        self.setLayout(layout)
        self.plot_graph()    

    
    def load_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select CSV", "", "CSV Files (*.csv);;All Files (*)")
        if not file_name:
            return

       
        self.temperatures = []
        self.revenues = []
        with open(file_name, 'r') as f:
            next(f)                                    
            for line in f:
                parts = line.strip().split(',')
                if len(parts) < 2:                     
                    continue
                self.temperatures.append(float(parts[0]))   
                self.revenues.append(float(parts[1]))

        self.plot_graph()

   
    def plot_graph(self):
        self.figure.clear()
        ax = self.figure.add_subplot()     

        
        ax.scatter(self.temperatures, self.revenues, s=1)   
        ax.spines['top'].set_visible(False)                
        ax.spines['right'].set_visible(False)              
        ax.set_title("Ice Cream Revenue vs. Outside Temperature")
        ax.set_xlabel("Temperature [°C]")
        ax.set_ylabel("Revenue [$]")

        if len(self.temperatures) >= 2:
            x = np.array(self.temperatures)
            y = np.array(self.revenues)

            m, b = np.polyfit(x, y, 1)

            x_line = np.linspace(x.min(), x.max(), 100)
            y_line = np.polyval([m, b], x_line)     
            ax.plot(x_line, y_line, color='red', linewidth=1.5, label='Trend line')

           
            ax.text(0.05, 0.92, f"$y = {m:.2f}x {b:+.2f}$",
                    transform=ax.transAxes, fontsize=12, color='red',
                    bbox=dict(boxstyle='round', facecolor='white', edgecolor='red'))
            ax.legend(loc='lower right')

        self.canvas.draw()      

    
    def show_about(self):
        self.about_window.show()     


if __name__ == "__main__":
    app = QApplication()
    qss_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.qss")
    with open(qss_path) as f:
        app.setStyleSheet(f.read())
    window = IceCreamWindow()
    window.show()
    app.exec()

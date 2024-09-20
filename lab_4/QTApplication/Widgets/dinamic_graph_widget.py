import pyqtgraph as pg
from PyQt5.QtWidgets import  QWidget, QVBoxLayout
from PyQt5.QtCore import QTimer

class DynamicGraphWidget(QWidget):
    """
    A widget for displaying a dynamic graph.
    """

    def __init__(self):
        super().__init__()

        self.plotWidget = pg.PlotWidget()
        self.plotWidget.showGrid(x=True, y=True)
        self.x_limit = 10
        layout = QVBoxLayout()
        layout.addWidget(self.plotWidget)
        self.setLayout(layout)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_graph)
        self.xs = [0]
        self.ys = [0]
        self.timer.start(10)
        self.curve = self.plotWidget.plot([],[], pen="r")

    def update_graph(self):
        """
        Updates the graph data with new values.
        """
        self.curve.setData(self.xs, self.ys)
        self.plotWidget.setLimits(xMin=self.xs[-1] - self.x_limit, xMax= self.xs[-1])
        if len(self.xs) >= self.x_limit*10:
            self.xs.pop(0)
            self.ys.pop(0)
# code for GUI
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pyqtgraph as pg
import sys

from preprocessing import Network


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        # configure App
        self.title = 'CZ4071 Project 1'
        # self.left = 100
        # self.top = 100
        # self.width = 600
        # self.height = 600
        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)

        # model class initialization
        self.network = Network()


        # initialize the Tabs
        self.createInputWidget()
        self.createGraphWidget()
        tab_widget = QTabWidget(self)

        # Add Tabs
        tab_widget.addTab(self.inputWidget, "Input")
        tab_widget.addTab(self.graphWidget, "Graph")

        # set Grid
        # layout = QGridLayout()
        # layout.addWidget(tab_widget, 0, 0)

        self.setCentralWidget(tab_widget)

        self.show()

    def createGraphWidget(self):
        self.graphWidget = pg.PlotWidget()
        # self.setCentralWidget(self.graphWidget)

        hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]

        # Add Background colour to white
        self.graphWidget.setBackground('w')
        # Add Title
        self.graphWidget.setTitle("Your Title Here")
        # Add Axis Labels
        self.graphWidget.setLabel(
            'left', 'Temperature (°C)', color='red', size=30)
        self.graphWidget.setLabel('bottom', 'Hour (H)', color='red', size=30)
        # Add legend
        self.graphWidget.addLegend()
        # Add grid
        self.graphWidget.showGrid(x=True, y=True)
        # Set Range
        self.graphWidget.setXRange(0, 10, padding=0)
        self.graphWidget.setYRange(20, 55, padding=0)

        pen = pg.mkPen(color=(255, 0, 0))
        self.graphWidget.plot(hour, temperature, name="Sensor 1",
                              pen=pen, symbol='+', symbolSize=30, symbolBrush=('b'))

    def createInputWidget(self):
        input_grid = QHBoxLayout()
        # Set Label
        # label = QLabel('Conferences to Include')
        # label.setFixedSize(200, 20)
        # font = label.font()
        # font.setBold(True)
        # label.setFont(font)
        # self.input_grid.addWidget(label, 0, 0)

        # Create conferences Checkboxes
        groupbox1 = QGroupBox("Conferences to Include")
        input_grid.addWidget(groupbox1)

        gridLayout = QGridLayout()
        groupbox1.setLayout(gridLayout)

        conf_list = self.network.getConferences()
        self.list_check_box = [i for i in range(len(conf_list))]
        for i, conf in enumerate(conf_list):
            self.list_check_box[i] = QCheckBox(conf)
            gridLayout.addWidget(self.list_check_box[i], i+1, 0)

        # Create questions dropdown list
        groupbox2 = QGroupBox("Questions to Analyze")
        input_grid.addWidget(groupbox2)
        qn_boxlayout = QVBoxLayout()
        groupbox2.setLayout(qn_boxlayout)

        qn_list = self.network.getQuestions()
        qn_combo_box = QComboBox()
        for j, qn in enumerate(qn_list):
            qn_combo_box.addItem(qn)

        qn_boxlayout.addWidget(qn_combo_box, alignment=Qt.AlignBottom)

        # Add Run Button
        run_button = QPushButton("Run Analysis")
        run_button.clicked.connect(self.runOnClicked)
        qn_boxlayout.addWidget(run_button, alignment=Qt.AlignBottom)

        # create dummy widget to put into Tab widget
        self.inputWidget = QWidget()
        self.inputWidget.setLayout(input_grid)
      
    def runOnClicked(self):
        checked = [ind for ind, cb in enumerate(self.list_check_box) if cb.isChecked() ]      
        print(checked)
        print([self.network.getConferences()[i] for i in checked])


def main():
    app = QApplication([])
    screen = App()
    screen.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

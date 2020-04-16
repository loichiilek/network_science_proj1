# code for GUI
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pyqtgraph as pg
import sys
import time

from preprocessing import Network
from science import Science

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
        # self.network = Network()
        self.check_state = []
        self.science = Science()


        # initialize the Tabs
        self.createInputWidget()
        self.createGraphWidget()
        self.tab_widget = QTabWidget(self)

        # Add Tabs
        self.tab_widget.addTab(self.inputWidget, "Input")
        self.tab_widget.addTab(self.graphWidget, "Analysis")

        # set Grid
        # layout = QGridLayout()
        # layout.addWidget(self.tab_widget, 0, 0)

        self.setCentralWidget(self.tab_widget)

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
        self.input_widget_layout = QHBoxLayout()
        # Set Label
        # label = QLabel('Conferences to Include')
        # label.setFixedSize(200, 20)
        # font = label.font()
        # font.setBold(True)
        # label.setFont(font)
        # self.self.input_widget_layout.addWidget(label, 0, 0)

        # Create conferences Checkboxes
        self.input_groupbox1 = QGroupBox("Conferences to Include")

        self.input_widget_layout.addWidget(self.input_groupbox1)

        self.input_grid_layout = QGridLayout()
        self.input_groupbox1.setLayout(self.input_grid_layout)

        #  # Add Conferences Button
        #   self.add_conf_button = QPushButton("Add Conf")
        #   self.add_conf_button.clicked.connect(self.addConfOnClicked)

        self.updateCheckboxes()
        
        self.checkAllCheckboxes()
        # self.input_grid_layout.addWidget(self.add_conf_button,len(self.conf_check_box)+1,0,1,2)


        # Create questions dropdown list
        self.input_groupbox2 = QGroupBox("Questions to Analyze")
        self.input_widget_layout.addWidget(self.input_groupbox2)
        self.input_qn_box_layout = QVBoxLayout()
        self.input_groupbox2.setLayout(self.input_qn_box_layout)

        qn_list = self.science.network.getQuestions()
        self.input_qn_combo = QComboBox()
        for j, qn in enumerate(qn_list):
            self.input_qn_combo.addItem(qn)

        self.input_qn_box_layout.addWidget(self.input_qn_combo, alignment=Qt.AlignBottom)


        # Add Run Button
        self.run_button = QPushButton("Run Analysis")
        self.run_button.clicked.connect(self.runOnClicked)
        self.input_qn_box_layout.addWidget(self.run_button, alignment=Qt.AlignBottom)


        # create dummy widget to put into Tab widget
        self.inputWidget = QWidget()
        self.inputWidget.setLayout(self.input_widget_layout)
      

    def updateCheckboxes(self):
        conf_list = self.science.network.getConferences()
        self.conf_check_box = [i for i in range(len(conf_list))]
        self.conf_label = [i for i in range(len(conf_list))]

        # reset layout so that the new checklists can be shown
        for i in reversed(range(self.input_grid_layout.count())):
          self.input_grid_layout.itemAt(i).widget().deleteLater()

        for i, conf in enumerate(conf_list):
            self.conf_check_box[i] = QCheckBox(conf[0].upper())
            self.conf_label[i] = QLabel('Tier ' + str(conf[1]))

            # set checked or unchecked based on check_state
            if conf in [c[0] for c in self.check_state]:
                self.conf_check_box[i].setChecked([c[1] for c in self.check_state if c[0]==conf][0])

            self.input_grid_layout.addWidget(self.conf_check_box[i], i + 1, 0)
            self.input_grid_layout.addWidget(self.conf_label[i], i + 1, 1)

        # if hasattr(self,"check_state"):
        #     for i in range(len(self.check_state)):
        #         if self.check_state[i][0]
        #         self.conf_check_box[i].setChecked(
        #             self.conf_check_box[i].isChecked())

        # update add conf button that gets deleted
        self.add_conf_button = QPushButton("Add New Conf")
        self.add_conf_button.clicked.connect(self.addConfOnClicked)
        self.input_grid_layout.addWidget(self.add_conf_button, len(self.conf_check_box) + 1, 0, 1, 2)
        
        # update remove conf button that gets deleted
        self.remove_conf_button = QPushButton("Remove Existing Conf")
        self.remove_conf_button.clicked.connect(self.removeConfOnClicked)
        self.input_grid_layout.addWidget(self.remove_conf_button, len(self.conf_check_box) + 2, 0, 1, 2)


    def checkAllCheckboxes(self):
        for cb in self.conf_check_box:
            cb.setChecked(True)


    def uncheckAllCheckboxes(self):
        for cb in self.conf_check_box:
            cb.setChecked(False)


    def rememberCheckState(self):
        conf_list = self.science.network.getConferences()
        self.check_state = [i for i in range(len(self.conf_check_box))]
        for i in range(len(self.conf_check_box)):
            self.check_state[i] = (conf_list[i],self.conf_check_box[i].isChecked())

    
    def addConfOnClicked(self,to_add):
        self.createConfDialogue()

    def removeConfOnClicked(self, to_rem):
        self.removeConfDialogue()

    def createConfDialogue(self):
        self.dial_widget = QWidget()
        self.dial_widget.windowTitle = 'Add'
        self.dial_widget.setObjectName('Add')
        self.dial_widget.setWindowFlags(Qt.Window | Qt.Popup)
        
        # move to approximately center
        self.dial_widget.move(self.mapToGlobal(self.rect().center()) - QPoint(
          self.dial_widget.width()/4, self.dial_widget.height()/4))
        label1 = QLabel("Conference Name")
        label2 = QLabel("Tier:")
        self.name_line_edit = QLineEdit()
        self.tier_line_edit = QLineEdit()
        self.confirm_add_button = QPushButton('Add')
        self.close_add_button = QPushButton('Cancel')

        def confOnConfirm():
            # write to conference file
            self.science.network.addConference(
                [self.name_line_edit.text(), self.tier_line_edit.text()])
            self.dial_widget.close()
            self.rememberCheckState()
            self.updateCheckboxes()

        def confOnClose():
            self.dial_widget.close()

        self.confirm_add_button.clicked.connect(confOnConfirm)
        self.close_add_button.clicked.connect(confOnClose)

        dial_layout = QGridLayout()
        dial_layout.addWidget(label1, 0, 0)
        dial_layout.addWidget(self.name_line_edit, 0, 1,1,2)
        dial_layout.addWidget(label2, 1, 0)
        dial_layout.addWidget(self.tier_line_edit, 1, 1,1,2)
        dial_layout.addWidget(self.confirm_add_button, 2, 2)
        dial_layout.addWidget(self.close_add_button, 2, 1)

        # dial_layout.setColumnMinimumWidth(1, 200)
        self.dial_widget.setLayout(dial_layout)
        self.dial_widget.show()



    def removeConfDialogue(self):
        self.rem_widget = QWidget()
        self.rem_widget.setWindowFlags(Qt.Window | Qt.Popup)

        # move to approximately center
        self.rem_widget.move(self.mapToGlobal(self.rect().center()) - QPoint(
            self.rem_widget.width()/4, self.rem_widget.height()/4))
        label1 = QLabel("Conference to Delete")
        self.remove_line_edit = QLineEdit()
        self.confirm_remove_button = QPushButton('Remove')
        self.close_remove_button = QPushButton('Cancel')

        def remOnConfirm():
            self.rememberCheckState()
            self.science.network.removeConference(self.remove_line_edit.text())
            self.rem_widget.close()
            self.updateCheckboxes()

        def remOnClose():
            self.rem_widget.close()

        self.confirm_remove_button.clicked.connect(remOnConfirm)
        self.close_remove_button.clicked.connect(remOnClose)

        rem_layout = QGridLayout()
        rem_layout.addWidget(label1, 0, 0)
        rem_layout.addWidget(self.remove_line_edit, 0, 1, 1, 2)
        rem_layout.addWidget(self.confirm_remove_button, 1, 2)
        rem_layout.addWidget(self.close_remove_button, 1, 1)

        self.rem_widget.setLayout(rem_layout)
        self.rem_widget.show()
      

    def runOnClicked(self):
        checked = [ind for ind, cb in enumerate(self.conf_check_box) if cb.isChecked()]
        # print(checked)
        # print([self.science.network.getConferences()[i] for i in checked])
        conf_list_names = [self.science.network.getConferences()[i][0] for i in checked]
        conf_list = [self.science.network.getConferences()[i] for i in checked]
        self.science.network.getPublications(conf_list_names)
                      
        question = self.input_qn_combo.currentIndex()

        if question == 0:
            self.science.question1(conf_list)
        if question == 1:
            res = self.science.question2(conf_list)
            print(res)
        if question == 2:
            res = self.science.question3a(conf_list)
            print(res)
        if question == 3:
            self.science.question4(conf_list)

        # display the PICTURE and TEXT  
      
        self.tab_widget.setCurrentIndex(1)


def main():
    app = QApplication([])
    screen = App()
    screen.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

# code for GUI
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
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
        self.setWindowTitle(self.title)

        # model class initialization
        self.check_state = []
        self.conf_to_analyze_old = None
        self.science = Science()

        # initialize the Tabs
        self.createInputWidget()
        self.createAnalysisWidget()
        self.tab_widget = QTabWidget(self)

        # Add Tabs
        self.tab_widget.addTab(self.input_widget, "Input")
        self.tab_widget.addTab(self.analysis_widget, "Analysis")

        self.setCentralWidget(self.tab_widget)

        self.show()


    def createAnalysisWidget(self):

        self.graph_widget_layout = QVBoxLayout()
        self.graph_pic_label = QLabel()
        self.graph_pic_label.setScaledContents(True)
        self.graph_text_label = QLabel()
        self.graph_text_label.setWordWrap(True)
        self.graph_widget_layout.addWidget(self.graph_pic_label)
        self.graph_widget_layout.addWidget(self.graph_text_label)

       # create dummy widget to put into Tab widget
        self.analysis_widget = QWidget()
        self.analysis_widget.setLayout(self.graph_widget_layout)


    def createInputWidget(self):
        self.input_widget_layout = QHBoxLayout()

        # Create conferences Checkboxes
        self.input_groupbox1 = QGroupBox("Conferences to Include")

        self.input_widget_layout.addWidget(self.input_groupbox1)

        self.input_grid_layout = QGridLayout()
        self.input_groupbox1.setLayout(self.input_grid_layout)

        self.updateCheckboxes()


        # Create questions dropdown list
        self.input_groupbox2 = QGroupBox("Questions to Analyze")
        self.input_widget_layout.addWidget(self.input_groupbox2)
        self.input_qn_box_layout = QVBoxLayout()
        self.input_groupbox2.setLayout(self.input_qn_box_layout)

        qn_list = self.science.network.getQuestions()
        self.input_qn_combo = QComboBox()
        for j, qn in enumerate(qn_list):
            self.input_qn_combo.addItem(qn)

        self.input_qn_box_layout.addWidget(
            self.input_qn_combo, alignment=Qt.AlignBottom)

        # Add Run Button
        self.run_button = QPushButton("Run Analysis")
        self.run_button.clicked.connect(self.runOnClicked)
        self.input_qn_box_layout.addWidget(
            self.run_button, alignment=Qt.AlignBottom)

        # create dummy widget to put into Tab widget
        self.input_widget = QWidget()
        self.input_widget.setLayout(self.input_widget_layout)


    def updateCheckboxes(self):
        conf_list = self.science.network.getConferences()
        self.conf_check_box = [i for i in range(len(conf_list))]
        self.conf_label = [i for i in range(len(conf_list))]

        # reset layout so that the new checklists can be shown
        for i in reversed(range(self.input_grid_layout.count())):
            self.input_grid_layout.itemAt(i).widget().deleteLater()

        # add toggle all checkboxes button
        self.toggle_checkbox  = QCheckBox('Toggle')
        self.toggle_checkbox.clicked.connect(self.toggleCheckbox)
        self.input_grid_layout.addWidget(self.toggle_checkbox, 0, 0)

        # add all the checkboxes
        for i, conf in enumerate(conf_list):
            self.conf_check_box[i] = QCheckBox(conf[0].upper())
            self.conf_label[i] = QLabel('Tier ' + str(conf[1]))

            # set checked or unchecked based on check_state
            if conf in [c[0] for c in self.check_state]:
                self.conf_check_box[i].setChecked(
                    [c[1] for c in self.check_state if c[0] == conf][0])

            self.input_grid_layout.addWidget(self.conf_check_box[i], i + 1, 0)
            self.input_grid_layout.addWidget(self.conf_label[i], i + 1, 1)


        # update add conf button that gets deleted
        self.add_conf_button = QPushButton("Add New Conf")
        self.add_conf_button.clicked.connect(self.addConfOnClicked)
        self.input_grid_layout.addWidget(
            self.add_conf_button, len(self.conf_check_box) + 1, 0, 1, 2)

        # update remove conf button that gets deleted
        self.remove_conf_button = QPushButton("Remove Existing Conf")
        self.remove_conf_button.clicked.connect(self.removeConfOnClicked)
        self.input_grid_layout.addWidget(
            self.remove_conf_button, len(self.conf_check_box) + 2, 0, 1, 2)

    def checkAllCheckboxes(self):
        for cb in self.conf_check_box:
            cb.setChecked(True)

    def uncheckAllCheckboxes(self):
        for cb in self.conf_check_box:
            cb.setChecked(False)

    def toggleCheckbox(self):
        if self.toggle_checkbox.isChecked():
            self.checkAllCheckboxes()
        else:
            self.uncheckAllCheckboxes()


    def rememberCheckState(self):
        # remember the checkboxes state everytime the list is changed
        conf_list = self.science.network.getConferences()
        self.check_state = [i for i in range(len(self.conf_check_box))]
        for i in range(len(self.conf_check_box)):
            self.check_state[i] = (
                conf_list[i], self.conf_check_box[i].isChecked())


    def addConfOnClicked(self, to_add):
        self.createConfDialogue()


    def removeConfOnClicked(self, to_rem):
        self.removeConfDialogue()


    def createConfDialogue(self):
        # Create the add Conf dialogue box
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
            self.science.network.addConference(
                [self.name_line_edit.text(), self.tier_line_edit.text()])
            self.dial_widget.close()
            self.rememberCheckState()
            self.updateCheckboxes()

        def confOnClose():
            self.dial_widget.close()

        # Add button handlers
        self.confirm_add_button.clicked.connect(confOnConfirm)
        self.close_add_button.clicked.connect(confOnClose)

        # add all the layouts
        dial_layout = QGridLayout()
        dial_layout.addWidget(label1, 0, 0)
        dial_layout.addWidget(self.name_line_edit, 0, 1, 1, 2)
        dial_layout.addWidget(label2, 1, 0)
        dial_layout.addWidget(self.tier_line_edit, 1, 1, 1, 2)
        dial_layout.addWidget(self.confirm_add_button, 2, 2)
        dial_layout.addWidget(self.close_add_button, 2, 1)

        self.dial_widget.setLayout(dial_layout)
        self.dial_widget.show()


    def removeConfDialogue(self):
        # Create the remove Conf dialogue box
        self.rem_widget = QWidget()
        self.rem_widget.setWindowFlags(Qt.Window | Qt.Popup)

        # move to approximately center
        self.rem_widget.move(self.mapToGlobal(self.rect().center()) - QPoint(
            self.rem_widget.width()/4, self.rem_widget.height()/4))
        label1 = QLabel("Conference to Delete")
        
        # add buttons
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

        # add button handlers
        self.confirm_remove_button.clicked.connect(remOnConfirm)
        self.close_remove_button.clicked.connect(remOnClose)

        # add everything to layout
        rem_layout = QGridLayout()
        rem_layout.addWidget(label1, 0, 0)
        rem_layout.addWidget(self.remove_line_edit, 0, 1, 1, 2)
        rem_layout.addWidget(self.confirm_remove_button, 1, 2)
        rem_layout.addWidget(self.close_remove_button, 1, 1)

        self.rem_widget.setLayout(rem_layout)
        self.rem_widget.show()


    def runOnClicked(self):
        # get the checked checkboxes
        checked = [ind for ind, cb in enumerate(
            self.conf_check_box) if cb.isChecked()]

        self.conf_to_analyze_new = [self.science.network.getConferences()[i][0]
                                    for i in checked]

        # code to make sure won't rerun all the time
        if self.conf_to_analyze_new != self.conf_to_analyze_old:
            print("conference list changed, getting conferences from DBLP....")
            self.science.network.getPublications(self.conf_to_analyze_new)
        self.conf_to_analyze_old = self.conf_to_analyze_new

        # get question from UI
        question = self.input_qn_combo.currentIndex()
        conf_list = [self.science.network.getConferences()[i] for i in checked]

        # run processing
        if question == 0:
            text_result = self.science.question1(conf_list)
            pic_result = 'q1_image.png'
        if question == 1:
            text_result = self.science.question2(conf_list)
            pic_result = 'q2_image.png'
        if question == 2:
            text_result = self.science.question3a(conf_list)
            pic_result = 'q3a_image.png'
        if question == 3:
            text_result = self.science.question3b(conf_list)
            pic_result = 'q3b_image.png'
        if question == 4:
            text_result = self.science.question4(conf_list)
            pic_result = 'q4_image.png'

        # display the PICTURE and TEXT
        self.createAnalysis(pic_result, text_result)

        # change to the analysis tab
        self.tab_widget.setCurrentIndex(1)


    def createAnalysis(self, pic, text):
        # update the analysis tab with the analysis picture and text
        pixmap = QPixmap(pic)
        self.graph_pic_label.setPixmap(pixmap)
        self.graph_text_label.setText(text)


def main():
    app = QApplication([])
    screen = App()
    screen.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

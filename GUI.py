from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from main import find_duplicates, similarity_to_hashsize, delete_picture

""" taskbar icon
    Get rid of grid layout if possible
    Change Hash Function
    Enable Folder Drag and Drop
    show in folder, open image buttons for pictures
    Show stats (path, file size, similarity)
"""

SIMILARITY_LEVEL = 90
FOLDERPATH = ''
SPACE_SAVED = 0


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(600, 800)
        MainWindow.setWindowTitle(_translate("MainWindow", "DupeFinder"))
        MainWindow.setWindowIcon(QIcon('logo.png'))
        

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.centralwidget.setObjectName("centralwidget")
    

        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QRect(0, 171, 600, 629))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setStyleSheet("background-color: rgb(220, 220, 220);")

        
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 600, 629))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        
        self.scroll_GridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.scroll_GridLayout.setObjectName('scroll_GridLayout')



        #Folders
        self.Folder_Label = QLabel(self.centralwidget)
        self.Folder_Label.setGeometry(QRect(125, 40, 600, 22))
        self.Folder_Label.setObjectName("label")
        self.Folder_Label.setText(_translate("MainWindow", "Folder: "))

        self.Browse_Folder_Button = QPushButton(self.centralwidget)
        self.Browse_Folder_Button.setGeometry(QRect(20, 40, 100, 22))
        self.Browse_Folder_Button.setObjectName("Browse_Folder_Button")
        self.Browse_Folder_Button.setText(_translate("MainWindow", "Browse Folders"))
        self.Browse_Folder_Button.setStyleSheet("background-color: rgb(220, 220, 220);")
        self.Browse_Folder_Button.clicked.connect(self.open_folder)




        #Sliders
        self.Slider_Label = QLabel(self.centralwidget)
        self.Slider_Label.setGeometry(QRect(25, 73, 80, 22))
        self.Slider_Label.setObjectName("label")
        self.Slider_Label.setText(_translate("MainWindow", "Similarity"))

        self.Similarity_Slider = QSlider(self.centralwidget)
        self.Similarity_Slider.setSliderPosition(SIMILARITY_LEVEL)
        self.Similarity_Slider.setGeometry(QRect(115, 73, 160, 22))
        self.Similarity_Slider.setOrientation(Qt.Horizontal)
        self.Similarity_Slider.setObjectName("horizontalSlider")
        self.Similarity_Slider.setMinimum(10)
        self.Similarity_Slider.setMaximum(100)
        self.Similarity_Slider.setTickPosition(QSlider.TicksAbove)
        self.Similarity_Slider.setTickInterval(10)
        self.Similarity_Slider.valueChanged.connect(self.slider_change)

        self.similarity_text = QLabel(self.centralwidget)
        self.similarity_text.setGeometry(QRect(285, 73, 50, 22))
        self.similarity_text.setObjectName("similarity_edit")
        self.similarity_text.setText(_translate("MainWindow", str(SIMILARITY_LEVEL) + '%'))


        #Find Duplicate Button
        self.Find_Dupes_Button = QPushButton(self.centralwidget)
        self.Find_Dupes_Button.setGeometry(QRect(20, 100, 100, 23))
        self.Find_Dupes_Button.setObjectName("pushButton")
        self.Find_Dupes_Button.setText(_translate("MainWindow", "Find Duplicates"))
        self.Find_Dupes_Button.setStyleSheet("background-color: rgb(220, 220, 220);")
        self.Find_Dupes_Button.clicked.connect(self.get_dupes)
    
        #Menu Bar
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 1600, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        self.statusbar = QStatusBar(self.centralwidget)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionOpen_Folder = QAction(self.centralwidget)
        self.actionOpen_Folder.setObjectName("actionOpen_Folder")
        self.menuFile.addAction(self.actionOpen_Folder)
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen_Folder.setText(_translate("MainWindow", "Open Folder"))
        self.actionOpen_Folder.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionOpen_Folder.triggered.connect(lambda: self.open_folder())

        self.actionRecent_Folders = QAction(self.centralwidget)
        self.actionRecent_Folders.setObjectName("actionRecent_Folders")
        self.menuFile.addAction(self.actionRecent_Folders)
        self.actionRecent_Folders.setText(_translate("MainWindow", "Recent Folders"))
        self.actionRecent_Folders.setShortcut(_translate("MainWindow", "Ctrl+Y"))
        self.menubar.addAction(self.menuFile.menuAction())
        QMetaObject.connectSlotsByName(MainWindow)

    def open_folder(self):
        global FOLDERPATH
        FOLDERPATH = QFileDialog.getExistingDirectory()
        newtext = "Folder: "+ str(FOLDERPATH)
        self.Folder_Label.setText(newtext)

    def no_folder_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Dupefinder")
        msg.setText("No Folder Selected")
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowIcon(QtGui.QIcon('logo.png'))
        x = msg.exec()

    def slider_change(self):
        new_value = self.Similarity_Slider.value()
        global SIMILARITY_LEVEL
        SIMILARITY_LEVEL = new_value
        self.similarity_text.setText(str(new_value)+ '%')

    def get_dupes(self):
        if FOLDERPATH != '':
            self.clear_elements()
            duplicates, originals = find_duplicates(FOLDERPATH, similarity_to_hashsize(SIMILARITY_LEVEL))
            self.print_dupes(duplicates, originals)
        else:
            self.no_folder_popup()

    def print_dupes(self, duplicates, originals):
        #folder, Double click to open (or right click), size
        counter = 0
        orig_keys = originals.keys()
        for o_key in orig_keys:
            if o_key in duplicates:
                orig = originals[o_key]
                self.checkbox = QCheckBox(orig)
                self.checkbox.setCheckState(Qt.Unchecked)
                self.checkbox.setStyleSheet("background-color: rgb(120, 120, 120);")
                self.scroll_GridLayout.addWidget(self.checkbox, counter, 0, 1,1)
                counter += 1
                dupes = duplicates[o_key]
                for dupe in dupes:
                    self.checkbox = QCheckBox(dupe)
                    self.checkbox.setCheckState(Qt.Unchecked)
                    self.scroll_GridLayout.addWidget(self.checkbox, counter, 0, 1,1)
                    counter += 1
        self.create_del_button()
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

    #deletes first element in scrollArea
    def clear_elements(self):
        counter = 0
        item = self.scroll_GridLayout.itemAt(0)
        while item != None:
            widget = item.widget()
            widget.deleteLater()
            counter = counter + 1
            item = self.scroll_GridLayout.itemAt(counter)

    def delete_selected(self):
        selected = []
        counter = 0
        item = self.scroll_GridLayout.itemAt(counter)
        while item != None:
            widget = item.widget()
            if widget.isChecked():
                global SPACE_SAVED
                SPACE_SAVED += delete_picture(FOLDERPATH, widget.text())
                selected.append(widget)
            counter = counter + 1
            item = self.scroll_GridLayout.itemAt(counter)
        self.get_dupes()
        #make a popup window saying how much space is saved, and a pop
        if SPACE_SAVED == 0:
            self.none_selected_popup()
        else:
            self.space_saved_popup()
        SPACE_SAVED = 0

    def none_selected_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Dupefinder")
        msg.setText("Nothing Selected")
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowIcon(QtGui.QIcon('logo.png'))
        x = msg.exec()

    def space_saved_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Dupefinder")
        msg.setText("Space Saved: " + str(SPACE_SAVED))
        msg.setIcon(QMessageBox.Information)
        msg.setWindowIcon(QIcon('logo.png'))
        x = msg.exec()

    def create_del_button(self): #2 Buttons to delete pictures
        self.Del_Dupes_Button = QPushButton(self.centralwidget)
        self.Del_Dupes_Button.setGeometry(QRect(20, 130, 100, 23))
        self.Del_Dupes_Button.setObjectName("Del_Dupes_Button")
        self.Del_Dupes_Button.setText("Delete Selected")
        self.Del_Dupes_Button.setStyleSheet("background-color: rgb(220, 220, 220);")
        self.Del_Dupes_Button.clicked.connect(self.delete_selected)
        self.Del_Dupes_Button.show()
        

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

#python -m PyQt5.uic.pyuic -x test.ui -o asdf.py 
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from image_funcs import find_duplicates, similarity_to_hashsize, delete_picture, show_image, get_size, convert_size, get_similarity


FOLDERPATH = ''
SPACE_SAVED = 0
SIMILARITY_LEVEL = 90


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(600, 800)
        MainWindow.setWindowTitle(_translate("MainWindow", "DupeFinder"))
        MainWindow.setWindowIcon(QIcon('logo.png'))
        
        #basic setup
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



        #Folder Label and Button
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




        #Slider and Text
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

    #action for when open folder or browse folder is pressed
    def open_folder(self):
        global FOLDERPATH
        FOLDERPATH = QFileDialog.getExistingDirectory()
        newtext = "Folder: "+ str(FOLDERPATH)
        self.Folder_Label.setText(newtext)

    #creates a popup if no folder was selected
    def no_folder_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Dupefinder")
        msg.setText("No Folder Selected")
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowIcon(QIcon('logo.png'))
        x = msg.exec()

    #Controls Slider Actions
    def slider_change(self):
        new_value = self.Similarity_Slider.value()
        global SIMILARITY_LEVEL
        SIMILARITY_LEVEL = new_value
        self.similarity_text.setText(str(new_value)+ '%')

    #Called when find duplicates button is pressed
    def get_dupes(self):
        if FOLDERPATH != '':
            self.clear_elements()
            duplicates, originals = find_duplicates(FOLDERPATH, similarity_to_hashsize(SIMILARITY_LEVEL))
            self.print_dupes(duplicates, originals)
        else:
            self.no_folder_popup()

    #Creates text in the Scroll Area with Originals and Duplicates
    def print_dupes(self, duplicates, originals):
        #folder, Double click to open (or right click), size
        counter = 0
        orig_keys = originals.keys()
        self.create_labels()
        for o_key in orig_keys:
            if o_key in duplicates:
                orig = originals[o_key]
                self.checkbox = QCheckBox(orig)
                self.checkbox.setCheckState(Qt.Unchecked)
                self.checkbox.setStyleSheet("background-color: rgb(150, 150, 150);")
                self.scroll_GridLayout.addWidget(self.checkbox, counter, 0, 1,2)
                self.create_show_image_button(counter, orig)
                self.create_size_text(counter, orig)
                counter += 1
                dupes = duplicates[o_key]
                for dupe in dupes:
                    self.checkbox = QCheckBox(dupe)
                    self.checkbox.setCheckState(Qt.Unchecked)
                    self.scroll_GridLayout.addWidget(self.checkbox, counter, 0, 1,2)
                    self.create_show_image_button(counter, dupe)
                    self.create_size_text(counter, dupe)
                    self.create_imgsimilarity_text(counter, orig, dupe)
                    counter += 1
        self.create_del_button()
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

    #deletes all elements in scrollArea
    def clear_elements(self):
        counter = 0
        item = self.scroll_GridLayout.itemAt(0)
        while item != None:
            widget = item.widget()
            widget.deleteLater()
            counter = counter + 1
            item = self.scroll_GridLayout.itemAt(counter)

    #checks which boxes are checked and deletes the image accordingly
    def delete_selected(self):
        selected = []
        counter = 0
        space_saved = 0
        item = self.scroll_GridLayout.itemAt(counter)
        while item != None:
            widget = item.widget()
            if widget.isChecked():
                space_saved += delete_picture(FOLDERPATH, widget.text())
                selected.append(widget)
            counter = counter + 1
            item = self.scroll_GridLayout.itemAt(counter)
        self.get_dupes()
        #make a popup window saying how much space is saved or a popup that says that nothing was selected to delete
        if space_saved == 0:
            self.none_selected_popup()
        else:
            self.space_saved_popup(space_saved)
        global SPACE_SAVED
        SPACE_SAVED = 0

    #stops the selection of nothing to delete
    def none_selected_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Dupefinder")
        msg.setText("Nothing Selected")
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowIcon(QIcon('logo.png'))
        x = msg.exec()

    #make a popup window saying how much space is saved
    def space_saved_popup(self, space_saved):
        msg = QMessageBox()
        msg.setWindowTitle("Dupefinder")
        msg.setText("Space Saved: " + str(convert_size(space_saved)))
        msg.setIcon(QMessageBox.Information)
        msg.setWindowIcon(QIcon('logo.png'))
        x = msg.exec()

    #Creates delete button
    def create_del_button(self):
        self.Del_Dupes_Button = QPushButton(self.centralwidget)
        self.Del_Dupes_Button.setGeometry(QRect(130, 100, 100, 23))
        self.Del_Dupes_Button.setStyleSheet("background-color: rgb(220, 220, 220);")
        self.Del_Dupes_Button.setObjectName("Del_Dupes_Button")
        self.Del_Dupes_Button.setText("Delete Selected")
        self.Del_Dupes_Button.clicked.connect(self.delete_selected)
        self.Del_Dupes_Button.show()

    #Creates a button with the image that opens a photo viewer
    def create_show_image_button(self, counter, name):
        self.show_image_button = QPushButton()
        self.show_image_button.setStyleSheet("background-color: rgb(220, 220, 220);")
        self.show_image_button.setObjectName("show_image_button")
        self.show_image_button.setText("Show Image")
        self.scroll_GridLayout.addWidget(self.show_image_button, counter, 4, 1,1)
        self.show_image_button.clicked.connect(lambda: show_image(FOLDERPATH, name))

    
    #Displays the size of the image
    def create_size_text(self, counter, name):
        self.size_text = QLabel()
        self.size_text.setObjectName("size_Text")
        self.size_text.setText(get_size(FOLDERPATH, name))
        self.scroll_GridLayout.addWidget(self.size_text, counter, 2, 1,1)

    #Displays the similarity of the duplicate to the original
    def create_imgsimilarity_text(self, counter, orig, dupe):
        self.imgsimilarity_text = QLabel()
        self.imgsimilarity_text.setObjectName("similarity_text")
        self.imgsimilarity_text.setText(get_similarity(FOLDERPATH, orig, dupe))
        self.scroll_GridLayout.addWidget(self.imgsimilarity_text, counter, 3, 1, 1)

    #Creates Name, Size, Similarity Labels
    def create_labels(self):
        self.name_label = QLabel(self.centralwidget)
        self.name_label.setObjectName("name_label")
        self.name_label.setText("Name")
        self.name_label.setGeometry(QRect(75, 145, 100, 23))
        self.name_label.show()

        self.size_label = QLabel(self.centralwidget)
        self.size_label.setObjectName("size_label")
        self.size_label.setText("Size")
        self.size_label.setGeometry(QRect(260, 145, 100, 23))
        self.size_label.show()

        self.similarity_label = QLabel(self.centralwidget)
        self.similarity_label.setObjectName("similarity_label")
        self.similarity_label.setText("Similarity")
        self.similarity_label.setGeometry(QRect(370, 145, 100, 23))
        self.similarity_label.show()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

import sys

import mimetypes

#Anki
from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *

#PyQt4.Qt import Qt
from PyQt4 import QtGui

class FileWindow(QWidget):

    # main window of plugin
    def __init__(self):
        super(FileWindow, self).__init__()

        self.results = None
        self.thread = None

        self.initGUI()

    # create GUI skeleton
    def initGUI(self):
        
        self.box_top = QVBoxLayout()
        self.box_upper = QHBoxLayout()

        # left side
        self.box_left = QVBoxLayout()

        # quizlet url field
        self.box_name = QHBoxLayout()
        self.label_file = QLabel("Selected File:")
        self.label_filename = QLabel("C://test.txt")

        self.box_name.addWidget(self.label_file)
        self.box_name.addWidget(self.label_filename)

        # add layouts to left
        self.box_left.addLayout(self.box_name)

        # right side
        self.box_right = QVBoxLayout()

        # code (import set) button
        self.box_code = QHBoxLayout()
        self.button_code = QPushButton("Select File", self)
        self.box_code.addStretch(1)
        self.box_code.addWidget(self.button_code)
        """ self.button_code.clicked.connect(self.onCode) """

        # add layouts to right
        self.box_right.addLayout(self.box_code)

        # add left and right layouts to upper
        self.box_upper.addLayout(self.box_left)
        self.box_upper.addSpacing(20)
        self.box_upper.addLayout(self.box_right)

        # add all widgets to top layout
        self.box_top.addLayout(self.box_upper)
        self.box_top.addStretch(1)
        self.setLayout(self.box_top)

        # go, baby go!
        self.setMinimumWidth(500)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setWindowTitle("Automated Deck Updater")
        self.show()

# throw up window for notification
def message(title, message):
    QMessageBox.information(QWidget(), title, message)

# throw up a window with some info (used for testing)
def debug(message):
    QMessageBox.information(QWidget(), "Message", message)

# Select a file and check to see if it is a plain text file
def selectNewFile():
    filename = QtGui.QFileDialog.getOpenFileName()
    if filename == '':
        return None
    mime = mimetypes.guess_type(filename)
    if mime[0] == 'text/plain':
        return filename
    else:
        return None
# Test Function
def testFunction():
    filename = selectNewFile()
    if filename is None:
        debug("Try Again")
    else:
        debug(filename)    

def runPlugIn():
    global __window
    __window = FileWindow()

# Create a sub-menu item within menu to select text file
action = QAction("Automatic Text Updater", mw)
action.triggered.connect(runPlugIn)
mw.form.menuTools.addAction(action)
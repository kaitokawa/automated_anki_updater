import sys

import mimetypes, os, pickle

#Anki
from anki.importing import TextImporter
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
        self.label_filename = QLabel(checkOnStartUp())

        self.box_name.addWidget(self.label_file)
        self.box_name.addWidget(self.label_filename)

        # add layouts to left
        self.box_left.addLayout(self.box_name)

        # right side
        self.box_right = QVBoxLayout()

        # code (select) button
        self.box_select_code = QHBoxLayout()
        self.select_button_code = QPushButton("Select File", self)
        self.box_select_code.addStretch(1)
        self.box_select_code.addWidget(self.select_button_code)
        self.select_button_code.clicked.connect(self.onSelectCode)

        # code (remove) button
        self.box_remove_code = QHBoxLayout()
        self.remove_button_code = QPushButton("Remove File", self)
        self.box_remove_code.addStretch(1)
        self.box_remove_code.addWidget(self.remove_button_code)
        self.remove_button_code.clicked.connect(self.onRemoveCode)

        # code (create) button
        self.box_create_code = QHBoxLayout()
        self.create_button_code = QPushButton("Create New Deck", self)
        self.box_create_code.addStretch(1)
        self.box_create_code.addWidget(self.create_button_code)
        self.create_button_code.clicked.connect(self.onCreateCode)

        # add layouts to right
        self.box_right.addLayout(self.box_select_code)
        self.box_right.addLayout(self.box_remove_code)
        self.box_right.addLayout(self.box_create_code)

        # add left and right layouts to upper
        self.box_upper.addLayout(self.box_left)
        self.box_upper.addSpacing(20)
        self.box_upper.addLayout(self.box_right)

        # message label
        self.label_message = QLabel("\r\n")

        # add all widgets to top layout
        self.box_top.addLayout(self.box_upper)
        self.box_top.addWidget(self.label_message)
        self.box_top.addStretch(1)
        self.setLayout(self.box_top)

        # go, baby go!
        self.setMinimumWidth(500)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setWindowTitle("Automated Deck Updater")
        self.show()

    def onCreateCode(self):
        try:
            file = loadFromPickle()
            if file == '':
                message("Message", "There is no file to import from.")
            else:
                importFile(file)
        except EOFError:
            message("Message", "There is no file to import from.")

    def onRemoveCode(self):
        try:
            file = loadFromPickle()
            if file != '':
                self.label_filename.setText("<i>None")
                resetPicklePath()
                self.label_message.setText("Successfully removed.")
            else:
                message("Message", "There is no file to remove.")
        except EOFError:
            message("Message", "There is no file to remove.")

    def onSelectCode(self):
        # Select a file and check to see if it is a plain text file
        def selectNewFile():
            filename = QtGui.QFileDialog.getOpenFileName()
            if filename == '':
                return None
            mime = mimetypes.guess_type(filename)
            if mime[0] == 'text/plain':
                return filename
            else:
                message("Notice", "Please select a plain text file")
                return None

        def notifyUser():
            filename = selectNewFile()
            if filename is not None:
                self.label_filename.setText(filename.rsplit('/', 1)[-1])
                writeToPickle(filename)
                self.label_message.setText("Successfully Imported!")

        notifyUser()

# throw up window for notification
def message(title, message):
    QMessageBox.information(QWidget(), title, message)

# throw up a window with some info (used for testing)
def debug(message):
    QMessageBox.information(QWidget(), "Debug Message", message)   

def updateAtStartUp():
    try:
        textfile = loadFromPickle()
        if textfile != '':
            importFile(textfile)
    except EOFError:
        pass
    except IOError:
        pass

def checkOnStartUp():
    try:
        textfile = loadFromPickle()
        if textfile == '':
            return "<i>None"
        else:
            return textfile.rsplit('/', 1)[-1]
    except EOFError:
        return "<i>None"

def loadFromPickle():
    pickle_path = os.path.dirname(os.path.realpath(__file__)) + '\\file.pickle'
    textfile = ''
    try:
        with open(pickle_path, 'rb') as input:
            textfile = pickle.load(input)
    except EOFError:
        pass
    except IOError:
        pass
    return textfile

def writeToPickle(filepath):
    pickle_path = os.path.dirname(os.path.realpath(__file__)) + '\\file.pickle'
    if os.path.isfile(pickle_path):
        with open(pickle_path, 'rb') as input:
            textfile = pickle.load(input)
        textfile = filepath
        with open(pickle_path, 'wb') as output:
            pickle.dump(textfile, output, -1)
    else:
        textfile = filepath
        with open(pickle_path, 'wb') as output:
            pickle.dump(textfile, output, -1)

def resetPicklePath():
    pickle_path = os.path.dirname(os.path.realpath(__file__)) + '\\file.pickle'
    resetFile = ''
    with open(pickle_path, 'wb') as output:
        pickle.dump(resetFile, output, -1)

def importFile(filename):
    name = filename.rsplit('/', 1)[-1].rsplit('.', 1)[0]
    # select deck
    did = mw.col.decks.id(name)
    mw.col.decks.select(did)
    # anki defaults to the last note type used in the selected deck
    m = mw.col.models.byName("Basic")
    deck = mw.col.decks.get(did)
    deck['mid'] = m['id']
    mw.col.decks.save(deck)
    # and puts cards in the last deck used by the note type
    m['did'] = did
    # import into the collection
    ti = TextImporter(mw.col, filename)
    ti.initMapping()
    ti.run()
    mw.col.reset()
    mw.reset()

def runPlugIn():
    global __window
    __window = FileWindow()

# Create a sub-menu item within menu to open window
action = QAction("Automatic Text Updater", mw)
action.triggered.connect(runPlugIn)
mw.form.menuTools.addAction(action)
# Updates when Anki starts up
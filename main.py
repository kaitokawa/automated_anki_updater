import sys

import mimetypes, os, pickle
from os.path import expanduser

#Anki
from anki import Collection
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

        # file display field
        self.box_instr = QHBoxLayout()
        self.label_instr = QLabel("Everytime Anki opens, stored file will update.")

        self.box_instr.addWidget(self.label_instr)

        self.box_name = QHBoxLayout()
        self.label_file = QLabel("Selected File:")
        self.label_filename = QLabel(checkOnStartUp())

        self.box_name.addWidget(self.label_file)
        self.box_name.addWidget(self.label_filename)

        # message label
        self.label_message = QLabel("\r\n")

        # add layouts to left
        self.box_left.addLayout(self.box_instr)
        self.box_left.addLayout(self.box_name)
        self.box_left.addWidget(self.label_message)

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

        # add all widgets to top layout
        self.box_top.addLayout(self.box_upper)
        self.box_top.addStretch(1)
        self.setLayout(self.box_top)

        # adjust size of buttons
        self.select_button_code.setMinimumWidth(100)
        self.remove_button_code.setMinimumWidth(100)
        self.create_button_code.setMinimumWidth(100)

        # go, baby go!
        self.setMinimumWidth(500)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setWindowTitle("Automated Deck Updater")
        self.show()

    def onCreateCode(self):
        try:
            pickle_list = loadFromPickle()
            if not pickle_list:
                message("Message", "There is no file to import from.")
            else:
                importFile(pickle_list[0])
        except EOFError:
            message("Message", "There is no file to import from.")

    def onRemoveCode(self):
        try:
            pickle_list = loadFromPickle()
            if pickle_list:
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
            home = expanduser("~")
            filter = "Text files (*.txt)"
            filename = QtGui.QFileDialog.getOpenFileName(self, 'File Explorer', home, filter)
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
                resetPicklePath()
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
        pickle_list = loadFromPickle()
        try:
            if pickle_list[0] != '':
                importFileOutsideGUI(pickle_list[0])
        except IndexError:
            pass
    except EOFError:
        pass
    except IOError:
        pass

def checkOnStartUp():
    try:
        pickle_list = loadFromPickle()
        if not pickle_list:
            return "<i>None"
        else:
            return pickle_list[0].rsplit('/', 1)[-1]
    except EOFError:
        return "<i>None"

def loadFromPickle():
    pickle_path = os.path.dirname(os.path.realpath(__file__)) + '\\file.pickle'
    pickle_list = list()
    try:
        with open(pickle_path, 'rb') as input:
            pickle_list = pickle.load(input)
    except EOFError:
        pass
    except IOError:
        pass
    return pickle_list

def writeToPickle(filepath):
    pickle_list = list()
    pickle_path = os.path.dirname(os.path.realpath(__file__)) + '\\file.pickle'
    if os.path.isfile(pickle_path):
        with open(pickle_path, 'rb') as input:
            pickle_list = pickle.load(input)
        pickle_list.append(filepath)
        pickle_list.append(mw.pm.name)
        with open(pickle_path, 'wb') as output:
            pickle.dump(pickle_list, output, -1)
    else:
        pickle_list.append(filepath)
        pickle_list.append(mw.pm.name)
        with open(pickle_path, 'wb') as output:
            pickle.dump(pickle_list, output, -1)

def resetPicklePath():
    pickle_path = os.path.dirname(os.path.realpath(__file__)) + '\\file.pickle'
    reset_file = list()
    with open(pickle_path, 'wb') as output:
        pickle.dump(reset_file, output, -1)

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

def importFileOutsideGUI(filename):
    pickle_list = loadFromPickle()
    profile_name = pickle_list[1]
    anki_dir = os.path.dirname(os.path.realpath(__file__).rsplit('\\', 2)[0])
    anki_collection = anki_dir + '\\' + profile_name + '\collection.anki2'
    col = Collection(anki_collection)
    name = filename.rsplit('/', 1)[-1].rsplit('.', 1)[0]
    did = col.decks.id(name)
    col.decks.select(did)
    m = col.models.byName("Basic")
    deck = col.decks.get(did)
    deck['mid'] = m['id']
    col.decks.save(deck)
    m['did'] = did
    ti = TextImporter(col, filename)
    ti.initMapping()
    ti.run()
    col.reset()
    mw.reset()
    col.close()

def runPlugIn():
    global __window
    __window = FileWindow()

# Updates when Anki starts up
updateAtStartUp()
# Create a sub-menu item within menu to open window
action = QAction("Automatic Text Updater", mw)
action.triggered.connect(runPlugIn)
mw.form.menuTools.addAction(action)
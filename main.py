import sys

import mimetypes

#Anki
from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *

#PyQt4.Qt import Qt
from PyQt4 import QtGui

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
        showInfo("Try again")
    else:
        showInfo(filename)    

# Create a sub-menu item within menu to select text file
menu = QMenu("Automatic Text Updater", mw)
action = QAction("Select a New Text File", menu)
action.triggered.connect(testFunction)
mw.form.menuTools.addMenu(menu)
menu.addAction(action)
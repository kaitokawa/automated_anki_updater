from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *

# Test Function
def testFunction():
    showInfo("Test")

# Create a menu item to select text file
action = QAction("Select Text File", mw)
action.triggered.connect(testFunction)
mw.form.menuTools.addAction(action)
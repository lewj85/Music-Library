from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import QFileDialog
from implementation.primaries.GUI.helpers import get_base_dir
from implementation.primaries.GUI import MessageBox
from implementation.primaries.scripts.setup_script import do_setup
from implementation.primaries.exceptions import LilypondNotInstalledException
import os
from sys import platform
from implementation.primaries.GUI import themedWindow


class SetupWindow(QtGui.QDialog, themedWindow.ThemedWindow):

    def __init__(self, parent, theme, themes, design_folder):
        self.parent = parent
        QtGui.QDialog.__init__(self)
        themedWindow.ThemedWindow.__init__(self, theme, themes)
        self.design_folder = design_folder
        designer_file = os.path.join(self.design_folder, 'SetupWindow.ui')
        uic.loadUi(designer_file, self)
        self.refreshBtn.clicked.connect(self.refresh)
        self.browseBtn.clicked.connect(self.browse)

    def refresh(self):
        try:
            do_setup()
            self.hide()
        except LilypondNotInstalledException as e:
            messageBox = MessageBox.MessageBox(
                parent=self,
                message="Lilypond was not found",
                title="Lilypond error, default install")
            messageBox.show()

    def browse(self):
        if platform == "win32":
            path, filter = QFileDialog.getOpenFileNameAndFilter(
                self, caption="Select files to import", filter="Application (*.exe)")
        else:
            path, filter = QFileDialog.getOpenFileNameAndFilter(
                self, caption="Select files to import", filter="App file (*.app)")

        try:
            do_setup(path=path)
            fob = open(".path", 'w')
            fob.write(path)
            fob.close()
            self.hide()
        except LilypondNotInstalledException as e:
            messageBox = MessageBox.MessageBox(
                parent=self,
                message="Lilypond was not found",
                title="Lilypond error, custom install")
            messageBox.show()

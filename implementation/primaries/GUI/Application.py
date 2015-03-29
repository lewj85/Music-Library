from PyQt4 import QtCore, QtGui
import sys, os, pickle, threading, time
from implementation.primaries.GUI import StartupWidget, MainWindow, PlaylistDialog, renderingErrorPopup, ImportDialog
from implementation.primaries.ExtractMetadata.classes import MusicManager, SearchProcessor
from implementation.primaries.Drawing.classes import LilypondRender, MxmlParser, Exceptions


class Application(object):
    def __init__(self, app):
        self.app = app
        self.previous_collections = []
        self.col_file = ".collections"
        self.getPreviousCollections()
        self.SaveCollections()
        self.manager = None
        self.main = None
        self.folder = ""
        self.theme = "dark"
        if len(self.previous_collections) == 0:
             self.startUp()
        else:
            self.folder = self.previous_collections[-1]
            self.setupMainWindow()


    def startUp(self):
        self.folder = ""
        self.startup = StartupWidget.Startup(self)
        self.startup.show()



    def removeCollection(self, folder):
        if os.path.exists(os.path.join(folder, "music.db")):
            os.remove(os.path.join(folder, "music.db"))
        self.previous_collections.remove(folder)
        self.SaveCollections()


    def getPreviousCollections(self):
        try:
            col_fob = open(self.col_file, 'rb')
        except:
            self.SaveCollections()
            col_fob = open(self.col_file, 'rb')
        result_temp = pickle.load(col_fob)
        if result_temp is not None:
            self.previous_collections = result_temp
        return self.previous_collections

    def SaveCollections(self):
        col_fob = open(self.col_file, 'wb')
        pickle_obj = pickle.Pickler(col_fob)
        pickle_obj.dump(self.previous_collections)

    def addFolderToCollectionList(self, name):
        if name not in self.previous_collections:
            self.previous_collections.append(name)


    def FolderFetched(self, foldername):
        self.folder = foldername
        if self.folder != "":
            self.addFolderToCollectionList(foldername)
            self.SaveCollections()
            self.startup.close()
            self.setupMainWindow()

    def setupMainWindow(self):
        self.manager = MusicManager.MusicManager(folder=self.folder)
        self.updateDb()
        self.main = MainWindow.MainWindow(self)
        self.main.show()

    def getPlaylistFileInfo(self, playlist):
        return self.manager.getPlaylistFileInfo(playlist)

    def getFileInfo(self, filename):
        file_info = self.manager.getFileInfo(filename)
        return file_info

    def loadUserPlaylistsForAGivenFile(self, filename):
        data = self.manager.getPlaylistByFilename(filename)
        return data

    def loadFile(self, filename):
        '''
        This method should:
        - setup a renderer object
        - run it
        - return the pdf location
        :return: filename of generated pdf
        '''
        pdf_version = filename.split(".")[0]+".pdf"
        if os.path.exists(os.path.join(self.folder, pdf_version)):
            return os.path.join(self.folder, pdf_version)
        else:
            errorList = self.startRenderingTask(filename)
            pdf = os.path.join(self.folder, pdf_version)
            if not os.path.exists(pdf):
                errorList.append("file rendering failed to produce a pdf, check above errors")
            if len(errorList) > 0:
                self.errorPopup(errorList)
            if os.path.exists(pdf):
                return pdf

    def importPopup(self):
        dialog = ImportDialog.ImportDialog(self, self.theme)
        dialog.setWindowFlags(QtCore.Qt.Dialog)
        dialog.exec()

    def copyFiles(self, fnames):
        self.manager.copyFiles(fnames)
        self.updateDb()
        self.main.onSortMethodChange()
        self.main.loadPlaylists()

    def errorPopup(self, errors):
        popup = renderingErrorPopup.RenderingErrorPopup(self, errors, self.theme)
        popup.setWindowFlags(QtCore.Qt.Dialog)
        popup.exec()

    def query(self, input):
        data = SearchProcessor.process(input)
        results = self.manager.runQueries(data)
        return results

    def startRenderingTask(self, filename):
        errorList = []
        parser = MxmlParser.MxmlParser()
        piece_obj = None
        try:
            piece_obj = parser.parse(os.path.join(self.folder,filename))
        except Exceptions.DrumNotImplementedException as e:
            errorList.append("Drum tab found in piece: this application does not handle drum tab.")
        except Exceptions.TabNotImplementedException as e:
            errorList.append("Guitar tab found in this piece: this application does not handle guitar tab.")

        if piece_obj is not None:
            try:
                loader = LilypondRender.LilypondRender(piece_obj, os.path.join(self.folder,filename))
                loader.run()
            except BaseException as e:
                errorList.append(str(e))
        return errorList

    def updateDb(self):
        self.manager.refresh()

    def makeNewCollection(self):
        self.main.close()
        self.startUp()

    def addPlaylist(self, data):
        self.manager.addPlaylist(data)

    def loadPieces(self, method="title"):
        summary_strings = self.manager.getPieceSummaryStrings(method)
        return summary_strings

    def getPlaylists(self, select_method="all"):
        results = self.manager.getPlaylists(select_method=select_method)
        return results

    def getCreatedPlaylists(self):
        results = self.manager.getPlaylistsFromPlaylistTable()
        return results

    def PlaylistPopup(self):
        popup = PlaylistDialog.PlaylistDialog(self, self.theme)
        popup.setWindowFlags(QtCore.Qt.Dialog)
        popup.exec()

    def removePlaylists(self, playlists):
        self.manager.deletePlaylists(playlists)

    def updatePlaylistTitle(self, new_title, old_title):
        self.manager.updatePlaylistTitle(new_title, old_title)

    def loadPlaylists(self):
        pass


def main():

    app = QtGui.QApplication(sys.argv)

    app_obj = Application(app)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

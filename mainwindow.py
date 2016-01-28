
import sys
from PyQt4 import QtCore, QtGui
from drawing import Drawing

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)

        self.drawing = Drawing()
        self.setCentralWidget(self.drawing)  #sets up a drawing object as the central widget for the mainwindow 

        self.createActions() #creates actions used in the mainwindow
        self.createMenus() #creates menus for the mainwindow
        
        #sets up the mainwindow's title and size
        self.setWindowTitle(self.tr("Drawing Program"))
        self.resize(800,600)
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def closeEvent(self, event):
        '''
        Creates an event that describes how to act when trying to close the window.
        If current drawing hasn't been saved, the program asks the user if they want to save 
        the drawing or discard it, and then it can close the window.
        '''
        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

    def open(self):
        '''
        Creates an event that describes how to act when trying to open a file.
        If current drawing hasn't been saved, the program asks the user if they want to save 
        the drawing or discard it, and then it can return to opening a file from the computer's file system.
        '''
        if self.maybeSave():
            fileName = QtGui.QFileDialog.getOpenFileName(self,self.tr("Open File"), QtCore.QDir.currentPath(),
                                                         self.tr("Text files (*.txt)"))
            try:
                self.drawing.openText(fileName)
            except:
                raise IOError

        
    def new(self):
        '''
        This method was created for the 'New'-action; it determines what happens when the user
        clicks 'New'; it calls the drawing's newImage-method.
        '''
        if self.maybeSave():
            self.drawing.newImage()
            
        

    def selectcolor(self):
        '''
        This method enables the user to change the color they are drawing with, using QColorDIalog
        '''
        color = QtGui.QColorDialog.getColor(self.drawing.penColor())
        newColor = QtGui.QColor(color)
        if newColor.isValid():
            self.drawing.setPenColor(newColor)

    def penWidth(self):
        '''
        This method inables the user to change the width of the pen they are drawing with
        '''
        newWidth, ok = QtGui.QInputDialog.getInteger(self, self.tr("Pen Width"),self.tr("Select pen width:"),
                                               self.drawing.penWidth(), 1, 50, 1)
        
        if ok:
            self.drawing.setPenWidth(newWidth)
            self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

          
            
    def createActions(self):
        '''
        Creates actions that the user can do in the mainwindow, and connects the actions to methods described 
        elsewhere in the program
        '''
        self.openAct = QtGui.QAction(self.tr("&Open..."), self)
        self.openAct.setShortcut(self.tr("Ctrl+O"))
        self.connect(self.openAct, QtCore.SIGNAL("triggered()"), self.open)
       
        self.saveAsAct = QtGui.QAction(self.tr("&Save As"), self)
        self.saveAsAct.setShortcut(self.tr("Ctrl+S"))
        self.connect(self.saveAsAct, QtCore.SIGNAL("triggered()"), self.save)

        self.exitAct = QtGui.QAction(self.tr("&Exit"), self)
        self.exitAct.setShortcut(self.tr("Ctrl+Q"))
        self.connect(self.exitAct, QtCore.SIGNAL("triggered()"), self, QtCore.SLOT("close()"))
        
        self.clearScreenAct = QtGui.QAction("&Clear Screen", self)
        self.clearScreenAct.setShortcut(self.tr("Ctrl+L"))
        self.connect(self.clearScreenAct, QtCore.SIGNAL("triggered()"), self.drawing.clearImage)

        self.selectcolorAct = QtGui.QAction(self.tr("&Select Color..."), self)
        self.connect(self.selectcolorAct, QtCore.SIGNAL("triggered()"), self.selectcolor)

        self.penWidthAct = QtGui.QAction(self.tr("Pen &Width..."), self)
        self.connect(self.penWidthAct, QtCore.SIGNAL("triggered()"), self.penWidth)
        
        self.lineAct = QtGui.QAction(self.tr("Draw Line"),self)
        self.connect(self.lineAct,QtCore.SIGNAL("triggered()"), self.drawing.changeToLine)
        
        self.rectAct = QtGui.QAction(self.tr("Draw Rectangle"),self)
        self.connect(self.rectAct,QtCore.SIGNAL("triggered()"), self.drawing.changeToRect)
        
        self.circAct = QtGui.QAction(self.tr("Draw Circle"),self)
        self.connect(self.circAct,QtCore.SIGNAL("triggered()"), self.drawing.changeToCircle)
        
        self.newScreenAct = QtGui.QAction(self.tr("&New"), self)
        self.newScreenAct.setShortcut(self.tr("Ctrl+N"))
        self.connect(self.newScreenAct, QtCore.SIGNAL("triggered()"), self.new)
        
        self.undoAct = QtGui.QAction(self.tr("&Undo"), self)
        self.undoAct.setShortcut(self.tr("Ctrl+U"))
        self.connect(self.undoAct, QtCore.SIGNAL("triggered()"), self.drawing.undostack.undo)
        
        
        self.getListAct = QtGui.QAction(self.tr("List of shapes..."), self)
        self.connect(self.getListAct, QtCore.SIGNAL("triggered()"), self.drawing.getShapeList)
        #this act was mainly done in purpose of testing that the shapeslist includes all of the visible shapes
        
        self.cbutton = QtGui.QPushButton(self)
        self.cbutton.setIcon(QtGui.QIcon('circle.png'))
        self.connect(self.cbutton, QtCore.SIGNAL("clicked()"), self.drawing.changeToCircle)

        
        self.rbutton = QtGui.QPushButton(self)
        self.rbutton.setIcon(QtGui.QIcon('rectangle.png'))
        self.connect(self.rbutton, QtCore.SIGNAL("clicked()"), self.drawing.changeToRect)

        
        self.lbutton = QtGui.QPushButton(self)
        self.lbutton.setIcon(QtGui.QIcon('line_normal_begin.png'))
        self.connect(self.lbutton, QtCore.SIGNAL("clicked()"), self.drawing.changeToLine)
        
        self.undobutton = QtGui.QPushButton('Undo')
        self.connect(self.undobutton, QtCore.SIGNAL("clicked()"), self.drawing.undostack.undo)
        
        

    def createMenus(self):
        '''
        Creates menus and toolbars to store the actions, and adds the actions to them
        '''

        self.fileMenu = QtGui.QMenu(self.tr("&File"), self)
        self.fileMenu.addAction(self.newScreenAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.optionMenu = QtGui.QMenu(self.tr("&Options"), self)
        self.optionMenu.addAction(self.undoAct)
        self.optionMenu.addAction(self.selectcolorAct)
        self.optionMenu.addAction(self.penWidthAct)
        self.optionMenu.addAction(self.lineAct)
        self.optionMenu.addAction(self.rectAct)
        self.optionMenu.addAction(self.circAct)
        self.optionMenu.addSeparator()
        self.optionMenu.addAction(self.clearScreenAct)
        
        self.optionMenu.addAction(self.getListAct)
        #this act was mainly done in purpose of testing that the shapeslist includes all of the visible shapes


        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.optionMenu)
        
        toolbar = self.addToolBar('draw')
        toolbar.addWidget(self.cbutton)
        toolbar.addWidget(self.rbutton)
        toolbar.addWidget(self.lbutton)
        toolbar.addWidget(self.undobutton)

    def maybeSave(self):
        '''
        This method keeps track of whether or not the drawn image has to be saved before continuing with methods
        that conflict with the current image.
        '''
        if self.drawing.isModified():
            ret = QtGui.QMessageBox.warning(self, "Warning",
                        self.tr("The image has been modified.\n"
                                "Do you want to save your changes?"),
                        QtGui.QMessageBox.Yes | QtGui.QMessageBox.Default,
                        QtGui.QMessageBox.No,
                        QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Escape)
            if ret == QtGui.QMessageBox.Yes:
                return self.save()
            elif ret == QtGui.QMessageBox.Cancel:
                return False

        return True
   
    def save(self):
        '''
        A method describing the saving of the current image into a text file
        '''
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File', 'untitled', self.tr("Text files (*.txt)"))
        if filename:
            fname = open(filename, 'w')
            fname.write(self.drawing.formTextList())
            fname.close()
            self.drawing.setModified(False)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

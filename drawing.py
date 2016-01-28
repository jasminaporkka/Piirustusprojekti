
import sys
from PyQt4 import QtCore, QtGui
from undocommands import CommandDrawLine, CommandDrawRect, CommandDrawCircle, CommandClearScreen
from readfile import Read_File


class Drawing(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
    
        self.modified = False
        self.mousehappening = False
        self.myPenWidth = 1
        self.myPenColor = QtGui.QColor(0, 0, 0)
        self.image = QtGui.QImage()
        self.lastPoint = QtCore.QPoint()
        self.rectangle = False
        self.circle = False
        self.line = False
        self.list = []
        self.undostack = QtGui.QUndoStack(self)
        self.oldImage = None
        self.path = QtGui.QPainterPath()
        self.readfile = Read_File()
        

    def setPenColor(self, newColor):
        '''
        sets the used pens's color with the color given as a parameter
        '''
        self.myPenColor = newColor

    def setPenWidth(self, newWidth):
        '''
        sets the used pens's width with the width given as a parameter
        '''
        self.myPenWidth = newWidth
        
    def newImage(self):
        '''
        clears the image; fills it with white color
        method is undoable, and it also clears the list of shapes in the image
        '''
        
        self.image.fill(QtGui.qRgb(255, 255, 255))
        
        self.modified = False
        self.update()
        self.emptyList()
        
    def clearImage(self):
        '''
        does the same as new image, but this method can be undone
        '''
        
        self.saveOldImage()
        
        cmd = CommandClearScreen(self, self.image, QtGui.qRgb(255, 255, 255), self.list)
        self.undostack.push(cmd)
        
        self.modified = True
        self.update()

    def mousePressEvent(self, event):
        '''
        handles the mouse press event; determines what happens when the left button is pressed down
        '''
        if event.button() == QtCore.Qt.LeftButton:
            self.lastPoint = event.pos()
            self.mousehappening = True

    def mouseMoveEvent(self, event):
        '''
        handles the mouse move event; determines what happens when the left button is pressed and the mouse moves
        across the screen
        '''
        if (event.buttons() & QtCore.Qt.LeftButton) and self.mousehappening:
            mousepos = event.pos()
            self.update()
            
            
    def mouseReleaseEvent(self, event):
        '''
        handles the mouse release event; determines what happens when the left button is released
        '''
        if event.button() == QtCore.Qt.LeftButton and self.mousehappening:
            
            if self.rectangle == False and self.circle == False:
                self.drawLineTo(event.pos())
            elif self.rectangle == True:
                self.drawRectangleTo(event.pos())
            elif self.circle == True:
                self.drawCircleTo(event.pos())
            
            self.mousehappening = False
                
    
    def paintEvent(self, event):
        '''
        takes into account the current event and draws it onto the image
        '''
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.drawImage(QtCore.QPoint(0, 0), self.image)
        painter.end()
        
    
    def resizeEvent(self, event):
        '''
        resizes the event to fit the size of the displayed image
        '''
        if self.width() > self.image.width() or self.height() > self.image.height():
            newWidth = max(self.width() + 128, self.image.width())
            newHeight = max(self.height() + 128, self.image.height())
            self.resizeImage(self.image, QtCore.QSize(newWidth, newHeight))
            self.update()

        QtGui.QWidget.resizeEvent(self, event)
    
    
        
    def drawLineTo(self, endPoint):
        '''
        draws a line on the image using mouse events and undo-functions
        '''
        
        self.saveOldImage()
        
        painter = QtGui.QPainter()
        painter.begin(self.image)
        painter.setPen(QtGui.QPen(self.myPenColor, self.myPenWidth,
                                  QtCore.Qt.SolidLine, QtCore.Qt.SquareCap,
                                  QtCore.Qt.MiterJoin))
      
        painter.setRenderHint(painter.Antialiasing,True)
        cmd = CommandDrawLine(self, painter, self.lastPoint, endPoint)
        self.undostack.push(cmd)
        painter.end()
        self.modified = True

        self.update()
        
        red = self.penColor().red()
        green = self.penColor().green()
        blue = self.penColor().blue()
        alpha = self.penColor().alpha()
        
        line = QtCore.QLine(self.lastPoint, endPoint)
        linenode = "l,"+str(red)+","+str(green)+","+str(blue)+","+str(alpha)+","+str(self.penWidth())+","+str(line.x1())+","+str(line.y1())+","+str(line.x2())+","+str(line.y2())
        
        self.list.append(linenode)
        
    
    
    def drawRectangleTo(self, endPoint):
        '''
        draws a rectangle on the image using mouse events and undo-functions
        '''
        
        self.saveOldImage()
        
        painter = QtGui.QPainter()
        painter.begin(self.image)
        painter.setPen(QtGui.QPen(self.myPenColor, self.myPenWidth,
                                  QtCore.Qt.SolidLine, QtCore.Qt.SquareCap,
                                  QtCore.Qt.MiterJoin))
        painter.setRenderHint(painter.Antialiasing,True)
        
        rect = QtCore.QRect(self.lastPoint.x(), self.lastPoint.y(), (endPoint.x()-self.lastPoint.x()), (endPoint.y()-self.lastPoint.y()))
        
        cmd = CommandDrawRect(self, painter, rect)
        self.undostack.push(cmd)
        
        painter.end()
        self.modified = True
        self.update()
        
        red = self.penColor().red()
        green = self.penColor().green()
        blue = self.penColor().blue()
        alpha = self.penColor().alpha()
        
        rectnode = "r,"+str(red)+","+str(green)+","+str(blue)+","+str(alpha)+","+str(self.penWidth())+","+str(rect.x())+","+str(rect.y())+","+str(rect.width())+","+str(rect.height())
        self.list.append(rectnode)
        
        
    def drawCircleTo(self, endPoint):
        '''
        draws a circle on the image using mouse events and undo-functions
        '''
        self.saveOldImage()
        
        painter = QtGui.QPainter()
        painter.begin(self.image)
        painter.setPen(QtGui.QPen(self.myPenColor, self.myPenWidth,
                                  QtCore.Qt.SolidLine, QtCore.Qt.SquareCap,
                                  QtCore.Qt.MiterJoin))
        painter.setRenderHint(painter.Antialiasing,True)
        
        rect = QtCore.QRect(self.lastPoint.x(), self.lastPoint.y(), (endPoint.x()-self.lastPoint.x()), (endPoint.y()-self.lastPoint.y()))
        
        cmd = CommandDrawCircle(self, painter, rect)
        self.undostack.push(cmd)
        
        painter.end()
        self.modified = True
        self.update()
        
        red = self.penColor().red()
        green = self.penColor().green()
        blue = self.penColor().blue()
        alpha = self.penColor().alpha()
        
        circnode = "c,"+str(red)+","+str(green)+","+str(blue)+","+str(alpha)+","+str(self.penWidth())+","+str(rect.x())+","+str(rect.y())+","+str(rect.width())+","+str(rect.height())
        
        self.list.append(circnode)
        
    
    
    def resizeImage(self, image, newSize):
        '''
        resizes the used image to fit the size of the displayed image
        '''
        self.saveOldImage()
        
        if image.size() == newSize:
            return

        newImage = QtGui.QImage(newSize, QtGui.QImage.Format_RGB32)
        newImage.fill(QtGui.qRgb(255, 255, 255))
        painter = QtGui.QPainter()
        painter.begin(newImage)
        painter.drawImage(QtCore.QPoint(0, 0), image)
        painter.end()
        self.image = newImage
    
    
    def isModified(self):
        '''
        Returns a boolean value indicating whether the drawing has been modified, or if it has been for eg. saved
        '''
        return self.modified


    def penColor(self):
        '''
        returns the value of the current pen color
        '''
        return self.myPenColor

    def penWidth(self):
        '''
        returns the value of the current pen width
        '''
        return self.myPenWidth
    
    def changeToRect(self):
        '''
        Changes the shape wanted to draw to rectangle
        '''
        self.rectangle = True
        self.circle = False
        self.line = False
        
    def changeToLine(self):
        '''
        Changes the shape wanted to draw to line
        '''
        self.rectangle = False
        self.circle = False
        self.line = True
        
    def changeToCircle(self):
        '''
        Changes the shape wanted to draw to circle
        '''
        self.circle = True
        self.rectangle = False
        self.line = False
    
    def getShapeList(self):
        '''
        returns a list of shapes included in the drawing
        print self.list was used as a test, so I could see if all shapes were included in the list
        '''
        #print self.list
        return self.list
    
    def addToList(self, node):
        '''
        adds the given node to list of shapes
        Is used in read_file, so that shapes drawn on the image are also added into the list of images currently
        shown on the screen.
        '''
        self.list.append(node)
        
    def emptyList(self):
        '''
        Empties the drawing's list of shapes
        '''
        self.list = []
        
    def setList(self, list):
        '''
        Replaces the drawing's current list of shapes with the list given as a parameter
        '''
        self.list = list
    
    def saveOldImage(self):
        '''
        saves the image before it is altered
        '''
        self.oldImage = self.image.copy()
        
    def getOldImage(self):
        '''
        returns the 'old image' aka the image before its last alteration
        '''
        return self.oldImage
    
    def replaceImage(self, image):
        
        self.image = image

        
    def formTextList(self):
        '''
        Forms a string of the list of shapes in self.list and returns it
        '''
        templist = self.list
        str = ""
        while len(templist) >0:
            if len(templist) ==1:
                str = str+templist.pop(0)
            else:
                str = str+templist.pop(0)+"/"
        
        return str
    
    def openText(self, fileName):
        '''
        Opens and reads the given textfile and gives it as a parameter to the draw_file method
        '''
        text = open(fileName).read()
        self.readfile.draw_file(self, text)
        self.modified = False
       
        
    def draw_line(self, pencolor, penwidth, linestart, lineend):
        '''
        Draws a line to the image with the given parameters. 
        Method is called from the draw_file method in read_file class
        '''
        path = QtGui.QPainterPath()
        painter = QtGui.QPainter()
        painter.begin(self.image)
        painter.setPen(QtGui.QPen(pencolor, float(penwidth),
                                  QtCore.Qt.SolidLine, QtCore.Qt.RoundCap,
                                  QtCore.Qt.RoundJoin))
        
        painter.setRenderHint(painter.Antialiasing,True)
        path.lineTo(lineend)
        painter.drawPath(path)
        painter.end()
        
        
        
    def draw_rect(self, pencolor, penwidth, rect):
        '''
        Draws a rectangle to the image with the given parameters. 
        Method is called from the draw_file method in read_file class
        '''
        path = QtGui.QPainterPath()
        painter = QtGui.QPainter()
        painter.begin(self.image)
        painter.setPen(QtGui.QPen(pencolor, float(penwidth),
                                  QtCore.Qt.SolidLine, QtCore.Qt.RoundCap,
                                  QtCore.Qt.RoundJoin))
        painter.setRenderHint(painter.Antialiasing,True)
        path.addRect(rect)
        painter.drawPath(path)
        painter.end()
        
    def draw_circle(self, pencolor, penwidth, rect):
        '''
        Draws a circle/ellipse to the image with the given parameters. 
        Method is called from the draw_file method in read_file class
        '''
        path = QtGui.QPainterPath()
        painter = QtGui.QPainter()
        painter.begin(self.image)
        painter.setPen(QtGui.QPen(pencolor, float(penwidth),
                                  QtCore.Qt.SolidLine, QtCore.Qt.RoundCap,
                                  QtCore.Qt.RoundJoin))
        painter.setRenderHint(painter.Antialiasing,True)
        path.addEllipse(rect)
        painter.drawPath(path)
        painter.end()
        
        

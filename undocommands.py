
import sys
from PyQt4 import QtCore, QtGui



class CommandDrawLine(QtGui.QUndoCommand):
    '''
    A undocommand class for the drawing's draw line-function
    It recieves the drawing object, the drawing object's painter and the line's start and endpoints as parameters
    '''
    
    def __init__(self, drawing, painter, startpoint, endpoint):
        super(CommandDrawLine, self).__init__()
        
        self.painter = painter
        
        self.start = QtCore.QPoint(startpoint)
        self.end = QtCore.QPoint(endpoint)
        self.drawing = drawing
        
    def redo(self):
        
        
        self.painter.drawLine(self.start, self.end)
        
        self.drawing.update()
        
       
    def undo(self):
        list = self.drawing.getShapeList()
        list.pop()
        
        self.drawing.replaceImage(self.drawing.getOldImage())
        self.drawing.update()
        #print "undo line" 
        #this was used to test the method
        
    
class CommandDrawRect(QtGui.QUndoCommand):
    '''
    A undocommand class for the drawing's draw rectangle-function
    It recieves the drawing object, the drawing object's painter and the rectangle to be drawn as parameters
    '''
    
    def __init__(self, drawing, painter, rect):
        super(CommandDrawRect, self).__init__()
        
        self.painter = painter
        self.rect = rect
        self.drawing = drawing
    
    def redo(self):
        self.painter.drawRect(self.rect)
    
    def undo(self):
        list = self.drawing.getShapeList()
        list.pop()
        self.drawing.replaceImage(self.drawing.getOldImage())
        self.drawing.update()
        #print "undo rect"
        #this was used to test the method
    
class CommandDrawCircle(QtGui.QUndoCommand):
    '''
    A undocommand class for the drawing's draw circle-function
    It recieves the drawing object, the drawing object's painter and the rectangle which the ellipse/circle 
    is drawn with, as parameters
    '''
    
    def __init__(self, drawing, painter, rect):
        super(CommandDrawCircle, self).__init__()
        
        self.painter = painter
        self.rect = rect
        self.drawing = drawing
        
    def redo(self):
        self.painter.drawEllipse(self.rect)
    
    def undo(self):
        list = self.drawing.getShapeList()
        list.pop()
        self.drawing.replaceImage(self.drawing.getOldImage())
        self.drawing.update()
        #print "undo circle"
        #this was used to test the method
    
class CommandClearScreen(QtGui.QUndoCommand):
    '''
    A undocommand class for the drawing's clear screen-function
    It recieves the drawing object, the drawing object's image and the color with which the image is covered with,
    as parameters
    '''
    
    def __init__(self, drawing, image, color, list):
        super(CommandClearScreen, self).__init__()
        
        self.drawing = drawing
        self.image = image
        self.color = color
        self.list = list
        
    def redo(self):
        self.image.fill(self.color)
        self.drawing.emptyList()
        
    def undo(self):
        self.drawing.replaceImage(self.drawing.getOldImage())
        self.drawing.update()
        self.drawing.setList(self.list)
        

        
        

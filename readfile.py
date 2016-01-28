
import sys
from PyQt4 import QtGui, QtCore

class Read_File(object):
    '''
    In this class the text file that has been opened in the main window, is read and analyzed, and the shapes listed
    in the text file are drawn onto the drawing's image
    '''
    
    def draw_file(self, drawing, input):
        
        self.input = input
        self.drawing = drawing
        
        self.drawing.newImage() #we want a clean image to draw on, therefore we have to wipe away whatever there is before we add these shapes 

        shapes = self.input.split("/") #here a list on all the shapes is formed, by splitting the text file from each /
        
        
    
        while len(shapes) >0:
            shape = shapes.pop(0)
            self.drawing.addToList(shape)
            shapecomponents = shape.split(",")
            shapetype = shapecomponents.pop(0)
            if shapetype == 'l': #if the shape is a line
                    red = int(shapecomponents.pop(0))
                    green = int(shapecomponents.pop(0))
                    blue = int(shapecomponents.pop(0))
                    alpha = int(shapecomponents.pop(0))
                    pencolor = QtGui.QColor(red, green, blue, alpha)
                    penwidth = int(shapecomponents.pop(0))
                    linestart = QtCore.QPoint(int(shapecomponents.pop(0)), int(shapecomponents.pop(0)))
                    lineend = QtCore.QPoint(int(shapecomponents.pop(0)), int(shapecomponents.pop(0)))
                    self.drawing.draw_line(pencolor, penwidth, linestart, lineend)
            elif shapetype == 'r': #if the shape is a rectangle
                    red = int(shapecomponents.pop(0))
                    green = int(shapecomponents.pop(0))
                    blue = int(shapecomponents.pop(0))
                    alpha = int(shapecomponents.pop(0))
                    pencolor = QtGui.QColor(red, green, blue, alpha)
                    penwidth = int(shapecomponents.pop(0))
                    rect = QtCore.QRectF(int(shapecomponents.pop(0)), int(shapecomponents.pop(0)), int(shapecomponents.pop(0)), int(shapecomponents.pop(0)))
                    self.drawing.draw_rect(pencolor, penwidth, rect)
            elif shapetype == 'c': #if the shape is a circle/ellipse
                    red = int(shapecomponents.pop(0))
                    green = int(shapecomponents.pop(0))
                    blue = int(shapecomponents.pop(0))
                    alpha = int(shapecomponents.pop(0))
                    pencolor = QtGui.QColor(red, green, blue, alpha)
                    penwidth = int(shapecomponents.pop(0))
                    rect = QtCore.QRectF(int(shapecomponents.pop(0)), int(shapecomponents.pop(0)), int(shapecomponents.pop(0)), int(shapecomponents.pop(0)))
                    self.drawing.draw_circle(pencolor, penwidth, rect) #call the draw_circle method in
                    
    
        
        
  
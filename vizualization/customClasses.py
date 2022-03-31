import pyqtgraph.opengl as gl
from OpenGL.GL import *

from pyqtgraph.opengl import GLViewWidget
from PyQt5 import QtCore

class GLViewWidgetWithText(GLViewWidget):
    def __init__(self, positionAndText =[] ):
        GLViewWidget.__init__(self)
        self.positionAndText = positionAndText
    def paintGL(self, *args, **kwds):
        GLViewWidget.paintGL(self, *args, **kwds)
        self.qglColor(QtCore.Qt.white)
        for posText in self.positionAndText :
            x = posText[0][0]
            y = posText[0][1]
            z = posText[0][2]
            text = posText[1]
            self.renderText(x, y, z, text)


class GLAxisItemOwn(gl.GLAxisItem):
    def __init__(self, size=None, antialias=True, glOptions='translucent'):
        gl.GLAxisItem.__init__(self, size, antialias, glOptions)

    def paint(self):
        self.setupGLState()

        if self.antialias:
            glEnable(GL_LINE_SMOOTH)
            glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

        glLineWidth(2.0)
        glBegin( GL_LINES )
        x,y,z = self.size()

        scaling = 0.5
        glColor4f(0, 0, 1, 1.0)  # z is green
        #v = [0, 0, 1, 1] # vector init also possible
        #glColor4fv(v)  # z is blue
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, scaling*z)

        glColor4f(0, 1, 0, 1.0)  # y is yellow
        glVertex3f(0, 0, 0)
        glVertex3f(0, scaling*y, 0)

        glColor4f(1, 0, 0, 1.0)  # x is blue
        glVertex3f(0, 0, 0)
        glVertex3f(scaling*x, 0, 0)
        glEnd()


class SegmentItem(GLAxisItemOwn):
    def __init__(self, size=None, antialias=True, glOptions='translucent', colorVec = [1,0,0,1], listEndPts = []):
        GLAxisItemOwn.__init__(self, size, antialias, glOptions)
        self.lineColor_ = colorVec # red color [R,G,B,transparency], all values in ranges [0,1]
        self.listEndPoints_ = listEndPts # can either be a list or np.array()

    def setLineColor(self, colorVec):
        self.lineColor_ = colorVec


    def paint(self):
        GLAxisItemOwn.paint(self)

        glLineWidth(3.0)
        glBegin(GL_LINES)

        for p in self.listEndPoints_:
            glColor4fv(self.lineColor_)  # segment line color
            glVertex3f(p[0][0],p[0][1],p[0][2]) # line always starts at origin
            glVertex3fv(p[1]) # end-point

        glEnd()


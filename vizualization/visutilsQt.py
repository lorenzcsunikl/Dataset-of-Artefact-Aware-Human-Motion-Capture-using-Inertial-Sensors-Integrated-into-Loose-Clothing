import PyQt5.QtWidgets as qtw
from PyQt5 import QtCore, QtGui

import pyqtgraph.opengl as gl

from pyqtgraph import Transform3D
from vizualization.customClasses import GLAxisItemOwn, SegmentItem, GLViewWidgetWithText
import numpy as np
import pyqtgraph as pg

# %% Visualization with pyqtgraph
colorVecs = [ [0.5, 1, 1, 1],
              [1, 0.5, 1, 1],
              [1, 1, 0.5, 1],
              [.5, 1., 0.5, 1],
              [ 1, .5, 0.5, 1],
              [ 0, .5, 0.5, 1],
              [*list(np.random.rand(3)),1],[*list(np.random.rand(3)),1],[*list(np.random.rand(3)),1],
              [*list(np.random.rand(3)),1],[*list(np.random.rand(3)),1],[*list(np.random.rand(3)),1],
              [*list(np.random.rand(3)),1],[*list(np.random.rand(3)),1],[*list(np.random.rand(3)),1],
              [*list(np.random.rand(3)),1],[*list(np.random.rand(3)),1],[*list(np.random.rand(3)),1],
              [*list(np.random.rand(3)),1],[*list(np.random.rand(3)),1],[*list(np.random.rand(3)),1],
              [*list(np.random.rand(3)),1],[*list(np.random.rand(3)),1],[*list(np.random.rand(3)),1],
             ]

class SkeletonViewer():
    def __init__(self,titlename="", annotations = [], comperators = []):
        self.titlename = titlename

        self.app = pg.mkQApp()
        self.app.aboutToQuit.connect(self.app.exit)

        self.qwidget = qtw.QWidget()
        self.qttimer = QtCore.QTimer()
        self.qttimer_sampling_time = 6


        self.annotations = annotations # set on ground which skeleton
        # create 3D viewer
        self.view = GLViewWidgetWithText(self.annotations)

        # create label line for output
        self.labelTitle = qtw.QLabel()
        self.labelTitle.setText( titlename )
        self.labelTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTitle.setFixedHeight(30)
        self.labelTitle.setFont(QtGui.QFont('Arial', 20))

        # create Buttons for control
        self.buttonUnconnect = qtw.QPushButton('disconnect from console',self.qwidget)
        self.buttonUnconnect.clicked.connect( self.app.exit )

        self.buttonSmallForward = qtw.QPushButton('t+1',self.qwidget)
        self.buttonSmallForward.clicked.connect(self.smallSkipforward)
        self.buttonForward = qtw.QPushButton('t++100',self.qwidget)
        self.buttonForward.clicked.connect( self.skipforward )
        self.buttonBigForward = qtw.QPushButton('t++1000',self.qwidget)
        self.buttonBigForward.clicked.connect( self.bigskipforward )

        self.buttonPause = qtw.QPushButton('Pause',self.qwidget)
        self.buttonPause.clicked.connect( self.manejarPausa)

        self.buttonSmallBackward= qtw.QPushButton('t-1',self.qwidget)
        self.buttonSmallBackward.clicked.connect( self.minus1 )
        self.buttonBackward= qtw.QPushButton('t--100',self.qwidget)
        self.buttonBackward.clicked.connect( self.skipbackward)
        self.buttonBigBackward= qtw.QPushButton('t--1000',self.qwidget)
        self.buttonBigBackward.clicked.connect( self.bigskipbackward)

        # _____________________
        # |   layoutH0        |
        # | ______________    |
        # || layoutV1_L   |   |
        # ||              |   |
        # ||              |   |
        # || ____________ |   |
        # |||            ||   |
        # |||   hBox2    ||   |
        # |||____________||   |
        # ||______________|   |
        # |___________________|

        layoutV1_L = QtGui.QVBoxLayout()
        layoutV1_L.addWidget(self.buttonUnconnect)
        layoutV1_L.addWidget(self.labelTitle)
        layoutV1_L.addWidget(self.view,100)

        hBox2 = QtGui.QHBoxLayout()
        hBox2.addWidget(self.buttonBigBackward)
        hBox2.addWidget(self.buttonBackward)
        hBox2.addWidget(self.buttonSmallBackward)
        hBox2.addWidget(self.buttonPause)
        hBox2.addWidget(self.buttonSmallForward)
        hBox2.addWidget(self.buttonForward)
        hBox2.addWidget(self.buttonBigForward)
        layoutV1_L.addLayout(hBox2)


        self.view.resize(1000, 800)
        # 3D create floor
        self.grid = gl.GLGridItem()
        self.view.addItem(self.grid)
        # create global origin
        self.origin = GLAxisItemOwn(size=QtGui.QVector3D(0.5,0.5,0.5))
        self.view.addItem(self.origin)


        self.qwidget.setLayout(layoutV1_L)
        self.qwidget.setWindowTitle('Video Comparison')
        self.qwidget.setGeometry(0, 1000, 1000, 800)
        self.qwidget.show()

        self.pause  = False
        self.skipper = 1  ## FAST FORWARD

        self.skels = []
        self.animationDatas = []
        self.colorvectors = [QtGui.QColor(255,255,255), QtGui.QColor(255,0,0),
                             QtGui.QColor(0,255,0)    , QtGui.QColor(0,0,255),
                             QtGui.QColor(255,255,0)  , QtGui.QColor(255,0,255),
                             QtGui.QColor(0,225,255)  , QtGui.QColor(0,128,128),
                             QtGui.QColor(255,153,0)  , QtGui.QColor(204,255,204),
                             QtGui.QColor(255,128,128), QtGui.QColor(51,153,102) ]

    def smallSkipforward(self):
        self.t +=1
        if self.t > self.nTime:
            self.t = self.t - self.nTime
    def skipforward(self):
        self.t +=100
        if self.t > self.nTime:
            self.t = self.t - self.nTime
    def bigskipforward(self):
        self.t +=1000
        if self.t > self.nTime:
            self.t = self.t - self.nTime


    def minus1(self):
        t = self.t
        t -=1
        if t < 0:
            self.t = self.nTime - 20
        else:
            self.t = t
    def skipbackward(self):
        t = self.t
        t -=100
        if t < 0:
            self.t = self.nTime - 200
        else:
            self.t = t
    def bigskipbackward(self):
        t = self.t
        t -=1000
        if t < 0:
            self.t = self.nTime - 200
        else:
            self.t = t

    def manejarPausa(self):
        self.pause = not self.pause

    def getOrigin(self):
        return self.origin


    def setSkeleton(self, skel):
        self.skels.append(skel)
        for skel_segs in self.skels[-1].segs:
            self.view.addItem( skel_segs)

    def update(self):
      if not self.pause :
        self.t += self.skipper

      for skel, aData in zip(self.skels, self.animationDatas):
        if (self.t < aData.nTime):
          skel.update(aData, self.t)

      labeltext = self.titlename +  "  Frame:" + str(self.t) + "/" + str(self.animationDatas[0].nTime)
      if self.pause:
        labeltext = labeltext + " PAUSED"
      self.labelTitle.setText( labeltext  )

      if self.t % self.nTime == 0 or self.t-1 > self.nTime :
        self.t = self.skipper

    def animate(self, list_aData):
      self.t = -self.skipper
      for skel, aData in zip(self.skels, list_aData):
          posNP = aData.seg[0].pos_g[:,0]
          pos = (posNP[0]+0.5, posNP[1]-0.2, 0.)
          self.annotations.append( (  pos  ,skel.Id) )

      self.animationDatas = list_aData
      self.nTime = self.animationDatas[0].nTime
      self.qttimer.timeout.connect(self.update)
      self.qttimer.start(self.qttimer_sampling_time)
      self.app.exec_()

    def updateAnimationData(self,list_aData):
      self.qttimer.stop()
      self.t = -self.skipper
      self.animationDatas = list_aData
      self.nTime = self.animationDatas[0].nTime
      self.qttimer.timeout.connect(self.update)
      self.qttimer.start(self.qttimer_sampling_time)
      print('ANIMATION DATA UPDATED')

    def online_animation(self):
      self.t = 0
      self.nTime = 1
      self.qttimer.timeout.connect(self.update_online_animation)

    def update_online_animation(self):
      self.t += 1
      labeltext = self.titlename +  "  Frame:" + str(self.t)

      if self.pause:
        labeltext = labeltext + " PAUSED"
      self.labelTitle.setText( labeltext  )

      if not self.pause:
        for skel, aData in zip(self.skels, self.animationDatas):
            skel.update(aData, 0)

    def update_online(self, animationData):
      if self.qttimer.isActive():
        self.qttimer.stop()
      self.animationDatas=animationData
      self.update_online_animation()




class Segments:
    pass

class DrawSkeleton():
    def __init__(self, cData, colorVec = [0,1, 1, 0.5], origin=[], nameId = "NoName"):
        self.segs = [Segments() for i in range(cData.nSegs)]
        self.Trafos = [Transform3D() for i in range(cData.nSegs)]
        self.Id = nameId
        self.cData = cData
        self.noPtsList = []
        for ii,iseg in enumerate(cData.segIdx2Name):
          if (cData.segIdx2Name[iseg] in self.noPtsList):
              listPoints = []
          else:
              listPoints = cData.segCalib[ii].points
          self.segs[ii] = SegmentItem(colorVec=colorVec, size=QtGui.QVector3D(0.1,0.1,0.1), listEndPts=listPoints)
          self.segs[ii].setParent(origin)
          self.segs[ii].name = cData.segIdx2Name[iseg]



    def update(self, aData, t):
        for n in range(len(self.segs)):
            self.segs[n].setTransform( QtGui.QMatrix4x4(aData.seg[n].T[:,t]) )

    def getSegments(self):
        return self.segs

    def getSegIdxByName(self, segName):
        return self.cData.segName2Idx[segName]

    def getSegNameByIdx(self, segIdx):
        return self.cData.segIdx2Name[segIdx]

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 14:31:21 2020

@author: lorenz
"""

import utils.DataHelpers as dh
import utils.RotationCalculus as rc
import numpy as np

def toStackedTransformmatrix(quat, pos):
    nSamp = quat.shape[1]

    return np.block( [
        [ 2*quat[0,:]**2 + 2*quat[1,:]**2 - 1            ] ,
        [ 2*quat[1,:]*quat[2,:] - 2*quat[0,:]*quat[3,:]  ] ,
        [ 2*quat[0,:]*quat[2,:] + 2*quat[1,:]*quat[3,:]  ] ,
        [ pos[0,:]                                       ] ,
        [ 2*quat[0,:]*quat[3,:] + 2*quat[1,:]*quat[2,:]  ] ,
        [ 2*quat[0,:]**2 + 2*quat[2,:]**2 - 1            ] ,
        [ 2*quat[2,:]*quat[3,:] - 2*quat[0,:]*quat[1,:]  ] ,
        [ pos[1,:]                                       ] ,
        [ 2*quat[1,:]*quat[3,:] - 2*quat[0,:]*quat[2,:]  ] ,
        [ 2*quat[0,:]*quat[1,:] + 2*quat[2,:]*quat[3,:]  ] ,
        [ 2*quat[0,:]**2 + 2*quat[3,:]**2 - 1            ] ,
        [ pos[2,:]                                       ] ,
        [  np.zeros((1, nSamp))                          ] ,
        [  np.zeros((1, nSamp))                          ] ,
        [  np.zeros((1, nSamp))                          ] ,
        [  np.ones((1, nSamp))                           ]
        ] )
# The transform matrix (4x4) looks like this:
    #[               posX] where RotationMatrix is 3x3
    #[RotationMatrix posY] posX, posY, posZ is each 1
    #[               posZ]
    #[0   0     0       1]

class structtype():
    pass

# %% Section for skeletons, function which creates a callable skeleton with metainformation,
def createSkeleton(skeletonDefiniton, path= None):
    # create skeletons
    cData = structtype()
    cData.segCalib = []
    cData.segTree = [] # tuple (idx prev segment, idx calib point where contected to)

    skeletonDefiniton( cData, c=structtype(), path= path )

    cData.nSegs = len(cData.segCalib)
    return cData

def addPoints2SegCalib(points, segCalibs):
    c = structtype()
    c.points = points
    segCalibs.append(c)
    return

origin = [0.0, 0.0, 0.0]
animation_q_root = np.array([ 0.5,  0.5, -0.5, -0.5])
# %%
# here the actual skeleton is created similiar to bvh file definition of skeleton
# c.Points are the actual endpoints which are at the end rendered in the animation
def UpperBodySkeletonDefiniton( cData, c=structtype(), path=None ):
    pelviswidith = 0.25
    pelvisdepth  = 0.10
    pelvisheight = 0.1
    backlength   = 0.5
    claviclelength = 0.05
    torsodepth = pelvisdepth * 1.3
    torsowidth = pelviswidith*1.2
    upperArmLength = 0.34
    foreArmLength = 0.24

    origin = [0.0, 0.0, 0.0]
    # 0 pelvis
    addPoints2SegCalib( [ ([-pelvisdepth*3/4, 0.0, 0.0], [pelvisdepth/4, 0.0, pelviswidith/2]),
        ([-pelvisdepth*3/4, 0.0, 0.0], [pelvisdepth/4, 0.0, -pelviswidith/2]),
        ([-pelvisdepth*3/4, 0.0, 0.0], [-0.25*pelvisdepth, pelvisheight, 0.0]) ],
                       cData.segCalib)
    cData.segTree.append((0,-1,0, 'Pelvis','Pelvis'))

    # 1 Back
    addPoints2SegCalib( [(origin, [-0.4*torsodepth, backlength , 0.0]),
            (origin, [0.0, 0.8*backlength , torsowidth/2]),
            (origin, [0.0, 0.8*backlength , -torsowidth/2]) ], cData.segCalib)
    cData.segTree.append((1,0,2, 'Back','Sternum'))

    # 2 R-Shoulder
    addPoints2SegCalib( [(origin, [0.1*torsodepth,0.0 , claviclelength]) ],
                       cData.segCalib)
    cData.segTree.append((2,1,1, 'R-Clavicle','R-Shoulder'))

    # 3 R-UpperArm
    addPoints2SegCalib( [(origin, [0.0, -upperArmLength , 0.0]) ], cData.segCalib)
    cData.segTree.append((3,2,0, 'R-Shoulder','R-Upperarm'))

    # 4 R-Forearm
    addPoints2SegCalib( [(origin, [0.0, -foreArmLength , 0.0]) ], cData.segCalib)
    cData.segTree.append((4, 3, 0, 'R-Elbow','R-Forearm'))

    # 5 R-Hand
    addPoints2SegCalib( [(origin, [0.0, -foreArmLength/4 , 0.0]) ], cData.segCalib)
    cData.segTree.append((5, 4, 0, 'R-Wrist','R-Hand'))

    # 6 L-Shoulder
    addPoints2SegCalib( [(origin, [0.1*torsodepth,0.0 , -claviclelength]) ] ,cData.segCalib)
    cData.segTree.append((6, 1, 2, 'L-Clavicle','L-Shoulder'))

    # 7 L-UpperArm
    addPoints2SegCalib( [(origin, [0.0, -upperArmLength , 0.0]) ], cData.segCalib)
    cData.segTree.append((7, 6, 0, 'L-Shoulder','L-Upperarm'))

    # 8 L-Forearm
    addPoints2SegCalib( [(origin, [0.0, -foreArmLength , 0.0]) ], cData.segCalib)
    cData.segTree.append((8, 7, 0, 'L-Elbow','L-Forearm'))

    # 9 R-Hand
    addPoints2SegCalib( [(origin, [0.0, -foreArmLength/4 , 0.0]) ], cData.segCalib)
    cData.segTree.append((9, 8, 0, 'L-Wrist','L-Hand'))

    cData.segIdx2Name   = { segLeaf[0]: segLeaf[-1] for segLeaf in cData.segTree}
    cData.segName2Idx   = { cData.segIdx2Name[k] : k for k in cData.segIdx2Name}
    return cData

def FullBodySkeletonDefiniton( cData, c=structtype(), path=None ):
    femurlength  = 0.45
    tibialength  = 0.45
    ankleheight = 0.1
    footlenght = 0.18
    origin = [0.0, 0.0, 0.0]
    cData = UpperBodySkeletonDefiniton(cData, c=c, path=path)
    # 10 R-Thigh
    addPoints2SegCalib( [(origin, [0.0, -femurlength, 0.0]),
            (origin, [0.0, -0.9*femurlength, -0.05]),
            (origin, [0.0, -0.9*femurlength, 0.05])], cData.segCalib)
    cData.segTree.append((10,0,0, 'R-Hip','R-Tigh'))

    # 11 R-Shank
    addPoints2SegCalib( [(origin, [0.0, -tibialength, 0.0]),
            (origin, [0.0, -0.8*tibialength, -0.05]),
            (origin, [0.0, -0.8*tibialength,  0.05])], cData.segCalib)
    cData.segTree.append((11,10,0, 'R-Knee','R-Shank'))

    # 12 R-Foot
    addPoints2SegCalib( [(origin, [footlenght, -ankleheight, 0.0])], cData.segCalib)
    cData.segTree.append((12,11,0, 'R-Ankle','R-Foot'))


    # 13 L-Thigh
    addPoints2SegCalib(  [(origin, [0.0, -femurlength, 0.0]),
            (origin, [0.0, -0.9*femurlength, -0.05]),
            (origin, [0.0, -0.9*femurlength, 0.05])], cData.segCalib)
    cData.segTree.append((13,0,1, 'L-Hip','L-Tigh'))


    # 14 L-Shank
    addPoints2SegCalib( [(origin, [0.0, -tibialength, 0.0]),
            (origin, [0.0, -0.9*tibialength, -0.05]),
            (origin, [0.0, -0.9*tibialength,  0.05])   ], cData.segCalib)
    cData.segTree.append((14,13,0, 'L-Knee','L-Shank'))

    # 15 R-Foot
    addPoints2SegCalib( [(origin, [footlenght, -ankleheight, 0.0])], cData.segCalib)
    cData.segTree.append((15,14,0, 'L-Ankle','L-Foot'))


    cData.segIdx2Name   = { segLeaf[0]: segLeaf[-1] for segLeaf in cData.segTree}
    cData.segName2Idx   = { cData.segIdx2Name[k] : k for k in cData.segIdx2Name}
    return cData

def correctUpperBodyQuats(quats,names):
    for ii, iname in enumerate(names):
        if iname in dh.invertForGraph.keys():
            if not dh.invertForGraph[iname] :
                quats[ii] = rc.quatUniInv(quats[ii])
        if iname in dh.jointDict:
            names[ii] = dh.jointDict[iname]
    return
# %%
# given quaternions and the names of the segment, as well as the skeleton
# the actual poses (orienation+position) are computed this equals the computation of the
# motion in the bvh file
def computeAnimationFromJointPoses(quats, names, cData=createSkeleton(UpperBodySkeletonDefiniton),
                                   rootposition = np.array([0. ,0., 0.8]), rootrotation=animation_q_root,
                                   correctionfunction=None, root_is_fixed = True ):
  if correctionfunction: # function if quats need to inverted or names to be changed
      correctionfunction(quats,names)

  aData = structtype()
  nSegs = cData.nSegs
  nTime = len(quats[0])
  seg = [structtype() for i in range(nSegs)]
  rootrotation = rootrotation /np.linalg.norm(rootrotation);
  rootrotation =  np.tile( rootrotation[:,None], (1,nTime))
  aData.segNames = []
  aData.jointNames =[]

  for ii in range(0, len(cData.segTree)):
    (segIdx, idx_segConntected2, idx_PointConnected2, jointName, segName) = cData.segTree[ii]

    seg[segIdx].pos_g   = np.tile( rootposition[:,None], (1,nTime))
    seg[segIdx].quat_sg = rootrotation
    seg[segIdx].T = np.zeros((16, nTime))

    aData.segNames.append( segName)
    aData.jointNames.append( jointName )
    if idx_segConntected2 == -1 :
        if not root_is_fixed :
          iQuat = names.index( segName )
          seg[segIdx].quat_sg = rc.quatprod(rootrotation,  quats[iQuat]).T
    else:
        if jointName not in names:
          ident_quat = np.column_stack( (np.ones(nTime), np.zeros( (nTime,3)) ) )
          quat = ident_quat
        else:
          iQuat = names.index( jointName )
          quat = quats[iQuat]

        seg2Joint = np.tile( np.array(cData.segCalib[idx_segConntected2].points[idx_PointConnected2][1])[:,None], (1,nTime) )
        seg[segIdx].pos_g   = seg[idx_segConntected2].pos_g + rc.rotateVectorArray(seg[idx_segConntected2].quat_sg, seg2Joint )
        seg[segIdx].quat_sg = rc.quatprod( seg[idx_segConntected2].quat_sg, quat ).T

    seg[segIdx].T = toStackedTransformmatrix(seg[segIdx].quat_sg,  seg[segIdx].pos_g)

  aData.seg = seg
  aData.nTime = nTime
  aData.nSegs = nSegs
  return aData

def computeAnimationFromAbsOrientations(quats, names, cData=createSkeleton(UpperBodySkeletonDefiniton),
                                   rootposition = np.array([0. ,0., 0.8]),
                                   rootrotation=np.array([0.707106781186548, 0.707106781186548, 0, 0]),
                                   correctionfunction=None ):
  if correctionfunction: # function if quats need to inverted or names to be changed
      correctionfunction(quats,names)

  aData = structtype()
  nSegs = cData.nSegs
  nTime = len(quats[0])
  seg = [structtype() for i in range(nSegs)]
  rootrotation = rootrotation /np.linalg.norm(rootrotation);
  rootrotation =  np.tile( rootrotation[:,None], (1,nTime))
  aData.segNames = []
  aData.jointNames =[]

  for ii in range(0, len(cData.segTree)):
    (segIdx, idx_segConntected2, idx_PointConnected2, jointName, segName ) = cData.segTree[ii]

    seg[segIdx].pos_g   = np.tile( rootposition[:,None], (1,nTime))
    seg[segIdx].quat_sg = rootrotation
    seg[segIdx].T = np.zeros((16, nTime))

    aData.segNames.append( segName)
    aData.jointNames.append( jointName )

    if idx_segConntected2 == -1 :
      iQuat = names.index( segName )
      seg[segIdx].quat_sg = rc.quatprod(rootrotation,  quats[iQuat]).T
    else:
      if segName not in names:
        ident_quat = np.column_stack( (np.ones(nTime), np.zeros( (nTime,3)) ) )
        quat = ident_quat
      else:
        iQuat = names.index( segName )
        quat = quats[iQuat]
      pos_seg2Joint = np.tile( np.array(cData.segCalib[idx_segConntected2].points[idx_PointConnected2][1])[:,None], (1,nTime) )
      seg[segIdx].pos_g   = seg[idx_segConntected2].pos_g + rc.rotateVectorArray(seg[idx_segConntected2].quat_sg, pos_seg2Joint )
      seg[segIdx].quat_sg = rc.quatprod(rootrotation,  quat).T
    seg[segIdx].T = toStackedTransformmatrix(seg[segIdx].quat_sg,  seg[segIdx].pos_g)

  aData.seg = seg
  aData.nTime = nTime
  aData.nSegs = nSegs
  return aData

# %% Plot the position of the joints
def getJointPositionsFromAnimation(animation, order_joints=[]):
  '''Takes the animation and outputs the position of the joints
  Input
    animation : animation from computeAnimationFromAbsOrientations or computeAnimationFromJointPoses
    order_joings : list of the order of joints that have to be plotted, if [] then all joints are plotted
  '''
  if order_joints:
      pos=np.empty( (len(order_joints), animation.seg[0].pos_g.shape[1] ,3) )
      for iSeg, jointName in enumerate(order_joints):
          try:
              idx = animation.jointNames.index( jointName )
          except:
              continue
          pos[iSeg] = animation.seg[idx].pos_g.T

  else:
      pos=np.empty( (animation.nSegs, animation.seg[0].pos_g.shape[1],3) )
      for iSeg, seg in enumerate(animation.seg) :
          pos[iSeg] = seg.pos_g.T
      order_joints=animation.jointNames

  return (pos, order_joints)

import matplotlib.pyplot as plt
import numpy as np


def set_axes_equal(ax):
  '''Make axes of 3D plot have equal scale so that spheres appear as spheres,
  cubes as cubes, etc..  This is one possible solution to Matplotlib's
  ax.set_aspect('equal') and ax.axis('equal') not working for 3D.

  Input
    ax: a matplotlib axis, e.g., as output from plt.gca().
  '''

  x_limits = ax.get_xlim3d()
  y_limits = ax.get_ylim3d()
  z_limits = ax.get_zlim3d()

  x_range = abs(x_limits[1] - x_limits[0])
  x_middle = np.mean(x_limits)
  y_range = abs(y_limits[1] - y_limits[0])
  y_middle = np.mean(y_limits)
  z_range = abs(z_limits[1] - z_limits[0])
  z_middle = np.mean(z_limits)

  # The plot bounding box is a sphere in the sense of the infinity
  # norm, hence I call half the max range the plot radius.
  plot_radius = 0.5*max([x_range, y_range, z_range])

  ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
  ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
  ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])

def plot_joint_positions(jointPositions, jointPositions_names, N_FIRST = 0, N_SAMP = 0, ax_existing= None):
  ''' Plots the joint Positions,
  Input
   jointPositions = list of Jointpositions computed by getJointPositionsFromAnimation()
   jointPositions_names = list of names corresponding to the order of JointPositions
   N_FIRST = idx of First frame in jointPositons
   N_SAMP = number of samples to be plotted N_FIRST : N_FIRST+N_SAMP
   ax_exiting = matplotlib ax object, if already exits
  '''
  if ax_existing == None:
    fig=plt.figure()
    ax_existing = fig.add_subplot(projection='3d')

  if N_SAMP == 0:
    N_SAMP = jointPositions[0].shape[0]
  for joint_pos, joint_name in zip(jointPositions, jointPositions_names):
    ax_existing.scatter(joint_pos[N_FIRST:N_FIRST+N_SAMP,0], joint_pos[N_FIRST:N_FIRST+N_SAMP,1], joint_pos[N_FIRST:N_FIRST+N_SAMP,2], s=100, label=joint_name )

  ax_existing.set_xlabel('X')
  ax_existing.set_ylabel('Y')
  ax_existing.set_zlabel('Z')
  set_axes_equal(ax_existing)



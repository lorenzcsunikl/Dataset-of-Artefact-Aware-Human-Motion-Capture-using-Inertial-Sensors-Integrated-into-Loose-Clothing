#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is an example application to vizualize the Dataset of
"Towards Artefact Aware Human Motion Capture using Inertial Sensors Integrated into Loose Clothing"
https://zenodo.org/record/5948725


@author: michael lorenz, lorenz@cs.uni-kl.de
"""

import addpaths
import utils.AnimationTools as ani
import vizualization.visutilsQt as vis
import h5py
import numpy as np


# %% Settings
IDX_PERSON = 1 # chose between Person 1 to 12
DIR_TO_H5 = 'DIR/TO/DATA'# -> Download the data From https://zenodo.org/record/5948725 <-
SEQUENCE = 'shoulder_flexion' # choose between ['longterm', 'shoulder_abduction', 'shoulder_flexion', 'squat']

showFullBody = True
# %% Load Data from files
# The order of quaternions are q = [q_w, q_x, q_y, q_z]
# Tight
H5_Filename= (DIR_TO_H5+ 'Tight_' +SEQUENCE+'.h5')
h5T = h5py.File(H5_Filename,'r')
quats_tight_rel = h5T['P'+str(IDX_PERSON)]['quatRel'][...]
quats_tight_abs = h5T['P'+str(IDX_PERSON)]['quatAbs'][...]
h5T.close()

# Loose
H5_Filename= (DIR_TO_H5+ 'Loose_' +SEQUENCE+'.h5')
h5L = h5py.File(H5_Filename,'r')
quats_loose_rel = h5L['P'+str(IDX_PERSON)]['quatRel'][...]
quats_loose_abs = h5L['P'+str(IDX_PERSON)]['quatAbs'][...]

#get the order of the quaternions
order_rel = [n.decode('utf-8')
              for n in list(h5L['P'+str(IDX_PERSON)]['orderRel'][...])]
order_abs = [n.decode('utf-8')
              for n in list(h5L['P'+str(IDX_PERSON)]['orderAbs'][...])]
h5L.close()

#the order corresponds to the quaternion in the list/array, first entry in order_rel is the first entry of the quaternions array
# %% prepare animation
# You can choose between a FullBody Skeleton or an Upper Body sekelton only
if showFullBody:
  skelData = ani.createSkeleton(ani.FullBodySkeletonDefiniton)
else:
  skelData = ani.createSkeleton(ani.UpperBodySkeletonDefiniton)

view = vis.SkeletonViewer(titlename= 'Trial: ' +SEQUENCE + ' Subject: ' + str(IDX_PERSON)) # initalize viewer
list_aData = [] # list that contains all animation data for each skeleton
skelstartPosition = -1
iaddPos = 0

def addSkel2Viewer(quatRels, label, iaddPos, rootPosition, computeAnimation):
    skel = vis.DrawSkeleton(skelData, vis.colorVecs[iaddPos], view.getOrigin(), nameId=label)
    view.setSkeleton(skel)
    rootposition = np.array([0. , iaddPos+rootPosition, 0.8])
    list_aData.append(computeAnimation(quatRels, rootposition ) )

# Use this if you want to use the relative/joint orientations for vizualization, position and orientation of the pelvis is fixed
computeAniRel = lambda x, rotpos : ani.computeAnimationFromJointPoses(x, order_rel, skelData, rootposition=rotpos,
                                                                            correctionfunction=ani.correctUpperBodyQuats)
addSkel2Viewer(quats_tight_rel, "Thight Rel", iaddPos, skelstartPosition, computeAniRel);
iaddPos+=1;
addSkel2Viewer(quats_loose_rel, "Loose Rel", iaddPos, skelstartPosition, computeAniRel);
iaddPos+=1;


# Use this if you want to use the absolute orientations for vizualization, only the position the pelvis is fixed
computeAniAbs = lambda x, rotpos : ani.computeAnimationFromAbsOrientations(x, order_abs, skelData,
                                                                           rootposition=rotpos, rootrotation=np.array([1, 0, 0, 0]))
addSkel2Viewer(quats_tight_abs, "Thight Abs", iaddPos, skelstartPosition, computeAniAbs);
iaddPos+=1;
addSkel2Viewer(quats_loose_abs, "Loose Abs", iaddPos, skelstartPosition, computeAniAbs);
iaddPos+=1;

# %% animate
# go through sequence and update skeleton
view.animate(list_aData)


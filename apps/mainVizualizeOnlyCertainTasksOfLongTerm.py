#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This is application vizualizs only certain tasks of the longterm trials contained in
 the Dataset of
"Towards Artefact Aware Human Motion Capture using Inertial Sensors Integrated into Loose Clothing"
https://zenodo.org/record/5948725


@author: michael lorenz, lorenz@cs.uni-kl.de
"""
import addpaths
import utils.AnimationTools as ani
import utils.DataHelpers as dh
import vizualization.visutilsQt as vis
import h5py
import numpy as np
import time


# %% Settings
IDX_PERSONS = [1,2] # chose between Person 1 to 12
DIR_TO_H5 = 'DIR/TO/DATA'# -> Download the data From https://zenodo.org/record/5948725 <-
SEQUENCE = 'longterm' # choose between ['longterm', 'shoulder_abduction', 'shoulder_flexion', 'squat']

showFullBody = True

print( 'All LongTerm activities')
print( dh.categLongTerm )

activities2TimeRange = dh.getActivationArray(IDX_PERSONS)
# %% Load Data from files
TAKE_ACTIVITY = 'S1Shelf2Ground'
for personAndTimeRange,idx_person in zip(activities2TimeRange,IDX_PERSONS):
  print('Person ' +str(idx_person))
  for timeRange in personAndTimeRange[TAKE_ACTIVITY]:
    beginning = timeRange[0]
    end = timeRange[1]
    print(beginning)
    print(end)
    # %%
    # The order of quaternions are q = [q_w, q_x, q_y, q_z]
    # Tight
    H5_Filename= (DIR_TO_H5+ 'Tight_' +SEQUENCE+'.h5')
    h5T = h5py.File(H5_Filename,'r')
    quats_tight_rel = h5T['P'+str(idx_person)]['quatRel'][:, beginning:end, :]
    h5T.close()

    # Loose
    H5_Filename= (DIR_TO_H5+ 'Loose_' +SEQUENCE+'.h5')
    h5L = h5py.File(H5_Filename,'r')
    quats_loose_rel = h5L['P'+str(idx_person)]['quatRel'][:, beginning:end, :]

    #get the order of the quaternions
    order_rel = [n.decode('utf-8')
                  for n in list(h5L['P'+str(idx_person)]['orderRel'][...])]
    h5L.close()

    #the order corresponds to the quaternion in the list/array, first entry in order_rel is the first entry of the quaternions array
    # %% prepare animation
    # You can choose between a FullBody Skeleton or an Upper Body sekelton only
    if showFullBody:
      skelData = ani.createSkeleton(ani.FullBodySkeletonDefiniton)
    else:
      skelData = ani.createSkeleton(ani.UpperBodySkeletonDefiniton)

    view = vis.SkeletonViewer(titlename=SEQUENCE + ' Subject:' + str(idx_person) + ' Subtask: ' + TAKE_ACTIVITY) # initalize viewer
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

    # %% animate
    # go through sequence and update skeleton
    view.animate(list_aData)
    view.app.exec_()



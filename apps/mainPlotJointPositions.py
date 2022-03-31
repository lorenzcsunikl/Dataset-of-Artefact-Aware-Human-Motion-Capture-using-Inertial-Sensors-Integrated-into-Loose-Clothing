#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is an example application to vizualize the joint positions of the trials in Dataset of
"Towards Artefact Aware Human Motion Capture using Inertial Sensors Integrated into Loose Clothing"
https://zenodo.org/record/5948725


@author: michael lorenz, lorenz@cs.uni-kl.de
"""

import addpaths
import utils.AnimationTools as ani
import h5py


# %% Settings
IDX_PERSON = 1 # chose between Person 1 to 12
DIR_TO_H5 = 'DIR/TO/DATA'# -> Download the data From https://zenodo.org/record/5948725 <-
SEQUENCE = 'squat' # choose between ['longterm', 'shoulder_abduction', 'shoulder_flexion', 'squat']

# %% Load Data from files
# The order of quaternions are q = [q_w, q_x, q_y, q_z]
# You can either display the absolute or relative orientations of the loose or tight setup, see mainVizualization_H5.py
H5_Filename= (DIR_TO_H5+ 'Tight_' +SEQUENCE+'.h5')
h5T = h5py.File(H5_Filename,'r')
quats_tight_rel = h5T['P'+str(IDX_PERSON)]['quatRel'][...]
order_rel = [n.decode('utf-8')
              for n in list(h5T['P'+str(IDX_PERSON)]['orderAbs'][...])]
h5T.close()
#the order corresponds to the quaternion in the list/array, first entry in order_rel is the first entry of the quaternions array
# %% prepare animation
# You can choose between a FullBody Skeleton or an Upper Body sekelton only
skelData = ani.createSkeleton(ani.FullBodySkeletonDefiniton)
animation = ani.computeAnimationFromJointPoses(quats_tight_rel, order_rel, skelData, correctionfunction=ani.correctUpperBodyQuats)

(pos, order_joints) = ani.getJointPositionsFromAnimation(animation )
ani.plot_joint_positions(pos, order_joints, N_FIRST = 1000, N_SAMP = 1000)


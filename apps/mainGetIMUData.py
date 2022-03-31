#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This is application show how to extract the accelerometer, gyroscope and magnetometer
measurements from  the Dataset of
"Towards Artefact Aware Human Motion Capture using Inertial Sensors Integrated into Loose Clothing"
https://zenodo.org/record/5948725


@author: michael lorenz, lorenz@cs.uni-kl.de
"""
import addpaths
import h5py
import matplotlib.pyplot as plt

# %% Settings
IDX_PERSON = 1 # chose between Person 1 to 12
DIR_TO_H5 = 'DIR/TO/DATA'# -> Download the data From https://zenodo.org/record/5948725 <-
SEQUENCE = 'shoulder_abduction' # choose between ['longterm', 'shoulder_abduction', 'shoulder_flexion', 'squat']

TAKE_SEGMENT = 'L-Forearm'
# choose from ['L-Forearm', 'L-Upperarm', 'L-Shoulder', 'R-Forearm', 'R-Upperarm', 'R-Shoulder',
#  'Sternum', 'Pelvis', 'L-Tigh', 'L-Shank', 'R-Tigh', 'R-Shank', 'Head', 'L-Hand', 'R-Hand', 'L-Foot', 'R-Foot']

# %% Load Data from files
getValuesOf = lambda h5, name : h5['P'+str(IDX_PERSON)][name]

# Tight
H5_Filename= (DIR_TO_H5+ 'Tight_' +SEQUENCE+'.h5')
h5T = h5py.File(H5_Filename,'r')
#get the order of the quaternions
order_abs = [n.decode('utf-8')
              for n in list(h5T['P'+str(IDX_PERSON)]['orderAbs'][...])]
idx_segment_take = order_abs.index(TAKE_SEGMENT)
acc_tight = getValuesOf(h5T, 'acc')[idx_segment_take,:,:]
gyr_tight = getValuesOf(h5T, 'gyr')[idx_segment_take,:,:]
mag_tight = getValuesOf(h5T, 'mag')[idx_segment_take,:,:]
h5T.close()

# Loose
H5_Filename= (DIR_TO_H5+ 'Loose_' +SEQUENCE+'.h5')
h5L = h5py.File(H5_Filename,'r')
acc_loose = getValuesOf(h5L, 'acc')[idx_segment_take,:,:]
gyr_loose = getValuesOf(h5L, 'gyr')[idx_segment_take,:,:]
mag_loose = getValuesOf(h5L, 'mag')[idx_segment_take,:,:]
h5L.close()
# %% plot measurements
plt.figure()
plt.plot(acc_tight,label='acc_tight')
plt.plot(acc_loose,':',label='acc_loose')
plt.legend()
plt.grid(True)
plt.title('Accelerometer measurements')

plt.figure()
plt.plot(gyr_tight,label='gyr_tight')
plt.plot(gyr_loose,':',label='gyr_loose')
plt.legend()
plt.grid(True)
plt.title('Gyroscope measurements')

plt.figure()
plt.plot(mag_tight,label='mag_tight')
plt.plot(mag_loose,':',label='mag_loose')
plt.legend()
plt.grid(True)
plt.title('Magnetometer measurements')

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 11:13:30 2020

@author: lorenz
"""
import numpy as np
import MathUtils as mt


def quatprod(Q,P) :
    if P.shape[0] == 4:
        P = P.T

    if Q.shape[0] == 4:
        Q = Q.T

    QP = np.column_stack( (P[:,0]*Q[:,0] - P[:,1]*Q[:,1] - P[:,2]*Q[:,2] - P[:,3]*Q[:,3],
                    P[:,0]*Q[:,1] + P[:,1]*Q[:,0] - P[:,2]*Q[:,3] + P[:,3]*Q[:,2],
                    P[:,0]*Q[:,2] + P[:,2]*Q[:,0] + P[:,1]*Q[:,3] - P[:,3]*Q[:,1],
                    P[:,0]*Q[:,3] - P[:,1]*Q[:,2] + P[:,2]*Q[:,1] + P[:,3]*Q[:,0] )  )
    QP = QP / mt.vecnorm(QP)[:,None]
    return QP


def quatUniInv(Q):
    if Q.ndim == 1 :
        Qinv = Q.copy()
        Qinv[1:4] = -Qinv[1:4]
        return Qinv
    if Q.shape[0] == 4:
        Qinv = Q.T.copy()
    else :
        Qinv = Q.copy()
    Qinv[:,1:4] *= -1
    return Qinv


def rotateVectorArray(quat,pos):
    return np.block( [
        [pos[0,:]*(2*quat[0,:]**2 + 2*quat[1,:]**2 - 1) - pos[1,:]*(2*quat[0,:]*quat[3,:] - 2*quat[1,:]*quat[2,:]) + pos[2,:]*(2*quat[0,:]*quat[2,:] + 2*quat[1,:]*quat[3,:])],
        [pos[1,:]*(2*quat[0,:]**2 + 2*quat[2,:]**2 - 1) + pos[0,:]*(2*quat[0,:]*quat[3,:] + 2*quat[1,:]*quat[2,:]) - pos[2,:]*(2*quat[0,:]*quat[1,:] - 2*quat[2,:]*quat[3,:])],
        [pos[2,:]*(2*quat[0,:]**2 + 2*quat[3,:]**2 - 1) - pos[0,:]*(2*quat[0,:]*quat[2,:] - 2*quat[1,:]*quat[3,:]) + pos[1,:]*(2*quat[0,:]*quat[1,:] + 2*quat[2,:]*quat[3,:])]
        ])

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 11:14:48 2020

@author: lorenz
"""

import numpy as np

def vecnorm(mat, ax = 1):
    return np.sum( np.abs(mat)**2,axis=ax)**(1./2)

def rms(mat, ax = 0):
    return (np.sum( np.abs(mat)**2,axis=ax) / mat.shape[ax] )**(1./2)


def skew(v) :
    Q = np.zeros((3,3))
    Q[0,0:3] = np.block( [     0, -v[2],  v[1]])
    Q[1,0:3] = np.block( [  v[2],    0 , -v[0]])
    Q[2,0:3] = np.block( [ -v[1],  v[0],  0   ])
    return Q

def matrix3_times_array3(a, matrix):
    if matrix.ndim >2:
        matrix = matrix.reshape((3,3))
    out_array = np.empty(a.shape)
    
    out_array[:,0] = matrix[0,0] * a[:,0] + matrix[0,1] * a[:,1] + matrix[0,2] * a[:,2]
    out_array[:,1] = matrix[1,0] * a[:,0] + matrix[1,1] * a[:,1] + matrix[1,2] * a[:,2]
    out_array[:,2] = matrix[2,0] * a[:,0] + matrix[2,1] * a[:,1] + matrix[2,2] * a[:,2]
    return out_array

def correlation_lags(in1_len, in2_len, mode='full'):
    r"""
    Calculates the lag / displacement indices array for 1D cross-correlation.

    Parameters
    ----------
    in1_size : int
        First input size.
    in2_size : int
        Second input size.
    mode : str {'full', 'valid', 'same'}, optional
        A string indicating the size of the output.
        See the documentation `correlate` for more information.

    See Also
    --------
    correlate : Compute the N-dimensional cross-correlation.

    Returns
    -------
    lags : array
        Returns an array containing cross-correlation lag/displacement indices.
        Indices can be indexed with the np.argmax of the correlation to return
        the lag/displacement.

    Notes
    -----
    Cross-correlation for continuous functions :math:`f` and :math:`g` is
    defined as:

    .. math ::

        \left ( f\star g \right )\left ( \tau \right )
        \triangleq \int_{t_0}^{t_0 +T}
        \overline{f\left ( t \right )}g\left ( t+\tau \right )dt

    Where :math:`\tau` is defined as the displacement, also known as the lag.

    Cross correlation for discrete functions :math:`f` and :math:`g` is
    defined as:

    .. math ::
        \left ( f\star g \right )\left [ n \right ]
        \triangleq \sum_{-\infty}^{\infty}
        \overline{f\left [ m \right ]}g\left [ m+n \right ]

    Where :math:`n` is the lag.

    Examples
    --------
    Cross-correlation of a signal with its time-delayed self.

    >>> from scipy import signal
    >>> rng = np.random.RandomState(0)
    >>> x = rng.standard_normal(1000)
    >>> y = np.concatenate([rng.standard_normal(100), x])
    >>> correlation = signal.correlate(x, y, mode="full")
    >>> lags = signal.correlation_lags(x.size, y.size, mode="full")
    >>> lag = lags[np.argmax(correlation)]
    """


    # calculate lag ranges in different modes of operation
    if mode == "full":
        # the output is the full discrete linear convolution
        # of the inputs. (Default)
        lags = np.arange(-in2_len + 1, in1_len)
    elif mode == "same":
        # the output is the same size as `in1`, centered
        # with respect to the 'full' output.
        # calculate the full output
        lags = np.arange(-in2_len + 1, in1_len)
        # determine the midpoint in the full output
        mid = lags.size // 2
        # determine lag_bound to be used with respect
        # to the midpoint
        lag_bound = in1_len // 2
        # calculate lag ranges for even and odd scenarios
        if in1_len % 2 == 0:
            lags = lags[(mid-lag_bound):(mid+lag_bound)]
        else:
            lags = lags[(mid-lag_bound):(mid+lag_bound)+1]
    elif mode == "valid":
        # the output consists only of those elements that do not
        # rely on the zero-padding. In 'valid' mode, either `in1` or `in2`
        # must be at least as large as the other in every dimension.


        # the lag_bound will be either negative or positive
        # this let's us infer how to present the lag range
        lag_bound = in1_len - in2_len
        if lag_bound >= 0:
            lags = np.arange(lag_bound + 1)
        else:
            lags = np.arange(lag_bound, 1)
    return lags
#!/usr/bin/env python
"""
minbeam.py

Given a set of ellipses (beams), find the smallest area ellipse
that encloses them all.

Copyright(C) 2021 by
Trey V. Wenger; tvwenger@gmail.com

GNU General Public License v3 (GNU GPLv3)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published
by the Free Software Foundation, either version 3 of the License,
or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

May 2021 - Trey V. Wenger - v1.0
"""

import numpy as np
from scipy.optimize import basinhopping
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

__version__ = "1.0"


def string_length(X, f1, f2):
    """
    Calculate the string length from f0 to X to f1

    Inputs:
        X :: (N, 2) array of scalars
            Cartesian positions of N points
        f1 :: (2,) array of scalars
            Cartesian position of one focus
        f2 :: (2,) array of scalars
            Carteisan position of other focus

    Returns: length
        length :: (N,) array of scalars
            String length for each point
    """
    # Distance between each X and f1
    dist1 = np.sqrt(np.sum((X[..., None] - f1[None]) ** 2.0, axis=1))

    # Distance between each X and f2
    dist2 = np.sqrt(np.sum((X[..., None] - f2[None]) ** 2.0, axis=1))

    # Total distance
    return dist1 + dist2


def focii_positions(sep, pa):
    """
    Calculate the Cartesian coordinates of the ellipse focii given
    their separation and position angle.

    Inputs:
        sep :: scalar
            Distance between focii
        pa :: scalar
            Position angle (radians)

    Returns: f1, f2
        f1 :: (2, 1) array of scalars
            Cartesian position of one focus
        f2 :: (2, 1) array of scalars
            Carteisan position of other focus
    """
    f1 = np.array([sep / 2.0 * np.cos(pa), sep / 2.0 * np.sin(pa)])
    f2 = np.array([-sep / 2.0 * np.cos(pa), -sep / 2.0 * np.sin(pa)])
    return f1, f2


def best_params(X, max_sep):
    """
    Find position angle and focii separation for smallest area
    ellipse that encloses given points.

    Inputs:
        X :: (N, 2) array of scalars
            Cartesian positions of N points
        max_sep :: scalar
            The maximum possible focii separation

    Returns: sep, pa
        sep :: scalar
            Best focii separation
        pa :: scalar
            Best position angle (radians)
    """

    def area(params):
        if params.ndim == 1:
            params = params[..., None]
        sep, pa = params
        f1, f2 = focii_positions(sep, pa)
        s = np.max(string_length(X, f1, f2), axis=0)
        return np.pi * s / 4.0 * np.sqrt(s ** 2.0 - sep ** 2.0)

    class BasinhoppingBounds:
        def __init__(self, xmin, xmax):
            self.xmin = xmin
            self.xmax = xmax

        def __call__(self, **kwargs):
            x = kwargs["x_new"]
            return np.all(x >= self.xmin) and np.all(x <= self.xmax)

    guess = [max_sep / 2.0, np.pi / 2.0]
    bounds = [(0.0, max_sep), (0.0, np.pi)]
    xmin = np.array([b[0] for b in bounds])
    xmax = np.array([b[1] for b in bounds])
    basin_bounds = BasinhoppingBounds(xmin, xmax)
    res = basinhopping(
        area,
        guess,
        minimizer_kwargs={"method": "L-BFGS-B", "bounds": bounds},
        accept_test=basin_bounds,
        niter=100,
    )
    return res.x


def minbeam(beams):
    """
    Given a set of ellipses (beams), return the smallest area
    ellipse that encloses them all.

    Inputs:
        beams :: (N, 3) array of scalars
            For each of N beams, (major, minor, pa)
            where major and minor are the major and minor axes,
            and pa is the rotation angle in radians.

    Returns: major, minor, pa
        major, minor, pa :: scalars
            The major axis, minor axis, and position angle
            of the minimum area enclosing ellipse.
    """
    beams = np.array(beams)
    if beams.ndim != 2 or beams.shape[1] != 3:
        raise ValueError("Invalid shape for beams")

    # sample each ellipse 1000 times
    theta = np.linspace(0.0, 2.0 * np.pi, 1000)
    beams_x = np.array(
        [
            beam[0] / 2.0 * np.cos(theta) * np.cos(beam[2])
            - beam[1] / 2.0 * np.sin(theta) * np.sin(beam[2])
            for beam in beams
        ]
    ).flatten()
    beams_y = np.array(
        [
            beam[0] / 2.0 * np.cos(theta) * np.sin(beam[2])
            + beam[1] / 2.0 * np.sin(theta) * np.cos(beam[2])
            for beam in beams
        ]
    ).flatten()
    X = np.array([beams_x, beams_y]).T

    # maximum possible separation is twice the largest major axis
    max_sep = 2.0 * np.max(beams[0:2])

    # calculate parameters that minimize area
    sep, pa = best_params(X, max_sep)

    # convert separation to major and minor axes
    f1, f2 = focii_positions(sep, pa)
    major = np.max(string_length(X, f1[..., None], f2[..., None]))
    minor = np.sqrt(major ** 2.0 - sep ** 2.0)
    return major, minor, pa


def plot(beams):
    """
    Return a figure showing the minimum area ellipse and all other
    ellipses.

    Inputs:
        beams :: list of list of scalars
            For each beam, a list of (major, minor, pa)
            where major and minor are the major and minor axes,
            and pa is the rotation angle in radians.

    Returns: fig
        fig :: matplotlib.Figure
            Figure containing the plot
    """
    fig, ax = plt.subplots()
    for beam in beams:
        patch = Ellipse(
            (0.0, 0.0),
            beam[0],
            beam[1],
            angle=np.rad2deg(beam[2]),
            fill=False,
            edgecolor="black",
            linewidth=1.0,
            alpha=0.2,
        )
        ax.add_artist(patch)
    major, minor, pa = minbeam(beams)
    patch = Ellipse(
        (0.0, 0.0),
        major,
        minor,
        angle=np.rad2deg(pa),
        fill=False,
        edgecolor="red",
        linewidth=2.0,
    )
    ax.add_artist(patch)
    ax.set_xlim(-1.2 * major, 1.2 * major)
    ax.set_ylim(-1.2 * major, 1.2 * major)
    ax.set_aspect("equal")
    return fig

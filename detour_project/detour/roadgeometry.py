import numpy as np


def angle_adjust(thetadiff):
    """Adjust a given angle difference so as to restrict it between
    -pi and pi radians. The procedure is described at
    https://rosettacode.org/wiki/Angle_difference_between_two_bearings """

    diff = (thetadiff) % (2 * np.pi)
    if diff >= np.pi:
        diff -= 2 * np.pi
    return diff


# vec_angle_adjust is a function that applies angle_adjust
# to entries of numpy arrays.
vec_angle_adjust = np.vectorize(angle_adjust)


def xy2ka(xs, ys):
    """Converts a given road from Cartesian coordinates to coordinates
    in Frenet frame described with curvature and arclength values as
    described in

    Castellano, Cetinkaya, Arcaini,
    'Analysis of raod representations in search-based testing of autonomous
    driving systems', in Proc. IEEE QRS, pp. 167-178, 2021 doi:10.1109/QRS54544.2021.00028.

    Conversion is done from (x,y) coordinates to initial orientation
    together with kappa (curvature) and arclength values of road sections.
    The number of kappas is 2 short of the number of given coordinates.
    The number of pieces is 1 short of the number of given coordinates."""
    xdiffs = np.diff(xs)
    ydiffs = np.diff(ys)

    thetas = np.arctan2(ydiffs, xdiffs)
    thetadiffs = vec_angle_adjust(np.diff(thetas))
    arclengths = np.sqrt(xdiffs ** 2 + ydiffs ** 2)
    kappas = thetadiffs / arclengths[:-1]

    return thetas[0], kappas, arclengths

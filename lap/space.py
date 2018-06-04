# This module handles constructing and using a political space from "ideal" data
# Individual ideology vectors are modelled as lists of tuples of the form:
#
#   (label :: string, dimension :: int, value :: double)
#
# and combined with their dimensions and some helper functions as the Ideology class.
# Note: Dimensions are NOT counted from zero.
from .mathematics import pca
import scipy.spatial.distance as distance
import numpy as np


# An object modelling a political vector space
class PolySpace:
    # Constructor for an empty space
    def __init__(self):
        # n is the number of dimensions in this political space
        self.n = 0
        # A dictionary that keeps track of which dimensions have which label
        self.mapping = {}
        # if there is no data, there can be no meaningful political space
        # (technically the span of the null vector or R^0)
        # Non-null space should be a matrix (list of ROW vectors) made up of the
        # principal components of this particular political space
        self.space = np.array([])

    # Takes an Ideology vector and finds the closest principal component
    # metric determines the distance to be minimized.
    #       euclidean: l-2 norm
    #       cosine: Cosine of the angle between the vector and eigenvector
    def compare(self, vector, metric="euclidean"):
        # First project the vector into local political space
        vector = self.project(vector)

        # Wrapper function to accept two vectors
        def f(x, y): return distance.norm(x - y)

        if metric == "euclidean":
            pass
        elif metric == "cosine":
            f = distance.cosine
        else:
            raise Exception("Invalid Metric")
        # Compare each principal component
        minimum = f(vector, self.space[0])
        v = self.space[0]
        for pc in self.space:
            d = f(vector, pc)
            if d < minimum:
                minimum = d
                v = pc
        # Return the closest component
        return v

    # Projects an ideology onto this space.
    # If the mappings are the same, does nothing.
    def project(self, vector):
        if vector.n == 0 or vector.mapping == self.mapping:
            return vector
        for t in vector:
            newvector = Ideology()
            # If a dimension overlaps, shift it up
            if t.vec[1] <= self.n and t.vec[0] not in self.mapping:
                new = t[1] + self.n
                if new > vector.n:
                    new = vector.n + 1
                newvector.add((t[0], new, t[2]))
            else:
                newvector.add(t)
        # At this point, newvector is sorted correctly and does not overlap

    # Adds an opinion vector to this political space
    # vector :: Ideology
    def add(self, vector):
        pass


class Ideology:
    def __init__(self, data=None):
        if(data == None):
            self.vec = []
        else:
            self.vec = data
        self.n = len(data)

    # add a new dimension and value to this ideology
    def add(self, dim):
        # must be a 3-tuple
        if  len(dim) != 3:
            return
        else:
            self.vec.append(dim)
            self.n = self.n + 1
            self.vec = sorted(self.vec, key=lambda x: x[1])

    # Return a NumPy vector representation of this Ideology
    def vector(self):
        values = []
        for label, dimension, value in self.vec:
            values.append(value)
        return np.array(values)



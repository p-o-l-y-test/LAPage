import numpy as np

# Takes a matrix (rows are data points, unless orientation is changed)
# and returns the eigenvectors and their associated eigenvalues of the
# associated covariance matrix as a list of tuples
#
# data :: numpy.ndarray
# orientation :: string
def pca(data, orientation="row"):
    if orientation != "row":
        data = data.transpose()
    # Get the average vector
    M = matrixmean(data)
    # Put the data in mean-deviation form
    mdata = []
    for vector in data:
        mdata.append(vector - M)
    data = np.array(mdata)
    # Find the inner product
    data = np.dot(data, data.transpose())
    # Get the eigenvectors and eigenvalues
    # TODO: Return ordered version
    eigs = np.linalg.eig(data)
    paired = [(eigs[0][i], eigs[1][i]) for i in range(len(eigs))]
    paired = sorted(paired, key=lambda x: x[0])
    return paired


# Takes a vector of data (rows = data points) and finds the average vector
def matrixmean(data):
    return sum(data) / len(data)
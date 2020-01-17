import numpy as np
import sys
import os


def gauss_jordan(data, transform):
    """ The gauss jordan elimination algorithm that turns an appended matrix representing
    a system of linear equations to a its reduced row echleon form and updates the rhs accordingly.
    Arguments:
    data: The appended matrix representing a system of linear equations
    transform: transformation function that calculates and applies a gauss transform to the appended matrix
    """
    # matrix representing the lhs of system of linear eq
    l_data = data[:, 0:-1]
    # vector representing the rhs of system of linear eq
    r_data = data[:, -1]
    n_rows, n_cols = l_data.shape
    i = j = 0
    while i < n_rows and j < n_cols:
        l_data, r_data = transform(l_data, r_data, i, j)
        i += 1
        j += 1
    return np.append(l_data, r_data.reshape(r_data.shape[0], 1), axis=1)


def reduce_to_diagonal(l_data, r_data, i, j):
    """
    The first step in gauss jordan elimination algorithm that turns an appended matrix representing
    a system of linear equations to a diagonal matrix and updates the rhs accordingly.
    :param l_data: matrix representing the lhs of system of linear eq
    :param r_data: matrix representing the rhs of system of linear eq
    :param i: row counter
    :param j: column counter
    :return: transformed l_data, r_data
    """
    alpha11 = l_data[i, j]
    a01 = l_data[:, j][0:i] / alpha11
    a12T = l_data[i, j + 1:]
    a21 = l_data[i + 1:, j] / alpha11
    A22 = l_data[i + 1:, j + 1:]
    A02 = l_data[0:i, j + 1:]
    b0 = r_data[0:i]
    beta1 = r_data[i]
    b2 = r_data[i + 1:]
    # for the next iteration assign the values to relevant parts of the partitioned matrix
    l_data[0:i, j + 1:] = A02 - np.outer(a01, a12T)
    l_data[i + 1:, j + 1:] = A22 - np.outer(a21, a12T)
    r_data[0:i] = b0 - beta1 * a01
    r_data[i + 1:] = b2 - beta1 * a21
    l_data[:, j][0:i] = np.zeros(a01.shape)
    l_data[i + 1:, j] = np.zeros(a21.shape)
    return l_data, r_data


def reduce_to_identity(l_data, r_data, i, j):
    """
    The second part of gauss jordan elimination that transforms diagonal matrix A to an identity matrix
    and updates the right-hand side accordingly
    :param l_data: matrix representing the lhs of system of linear eq
    :param r_data: matrix representing the rhs of system of linear eq
    :param i: row counter
    :param j: column counter
    :return: transformed l_data, r_data
    """
    alpha11 = l_data[i, j]
    beta1 = r_data[i]
    r_data[i] = beta1 / alpha11
    l_data[i, j] = 1
    return l_data, r_data


def main():
    file_name = sys.argv[1]
    orig_data = np.genfromtxt("./../../data/linal/" + file_name, delimiter=",")
    print("Original appended matrix: \n{}".format(orig_data))
    print("Appended matrix shape: {}".format(orig_data.shape))
    data = orig_data.copy()
    diagonal_matrix = gauss_jordan(data, reduce_to_diagonal)
    print("Diagonal matrix derived from the appended matrix:\n{}".format(diagonal_matrix))
    reduced_row_echleon_form = gauss_jordan(diagonal_matrix, reduce_to_identity)
    print("Reduced row echleon form of the appended matrix:\n{}".format(reduced_row_echleon_form))


if __name__ == "__main__":
    main()

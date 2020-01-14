import numpy as np
import sys


def gaussian_elimination(data):
    n_rows, n_cols = data.shape
    i = 0
    j = 0
    a_TL = data[0:i, 0:j]
    tl_rows, tl_cols = a_TL.shape
    while (tl_rows * tl_cols) < ((n_rows-1) * (n_cols-2)):
        # perform gaussian elimination to render an upper triangular matrix with the elements below the diagonal
        # elements in each column containing the multipliers
        alpha11 = data[i][j]
        a21 = data[i+1:, j]
        A22 = data[i+1:, j+1:-1]
        a12T = data[i, j+1:-1]
        l21 = a21 / alpha11
        data[i + 1:, j] = l21
        A22 = A22 - np.outer(l21, a12T)
        data[i + 1:, j + 1:-1] = A22
        # perform forward substitution on the rightmost column
        beta = data[:, -1]
        beta1 = beta[i]
        b2 = beta[i+1:]
        b2 = b2 - beta1 * l21
        data[i+1:, -1] = b2
        # next iteration
        i += 1
        j += 1
        a_TL = data[0:i, 0:j]
        tl_rows, tl_cols = a_TL.shape
    return data


def back_substitution(data):
    # we will march from the bottom up partitioning the matrix
    i = j = 0
    reverse_data = data[: : -1]
    u_BR = reverse_data[i:0, j:0]
    n_rows, n_cols = reverse_data.shape
    while i < n_rows and j < n_cols:
        gamma11 = reverse_data[i, -j-2]
        b2 = reverse_data[0:i, -1][: : -1]
        beta1 = reverse_data[i, -1]
        u12T = reverse_data[i, -j-1:-1]
        beta1 = beta1 - np.dot(u12T, b2)
        reverse_data[i, -1] = beta1 / gamma11
        i += 1
        j += 1
    return reverse_data[:, -1][:: -1]


def validate_solution(data, solution_vector):
    # extract the left part from the appended matrix.
    data_left = data[:, 0:-1]
    # extract the right part ( the one after the equals to in system of linear eq ) from the appended matrix
    # as a vector
    data_right = data[:, -1]
    solved_vector = np.dot(data_left, solution_vector)
    print("solved vector: {}".format(solved_vector))
    if np.array_equal(data_right, solved_vector):
        print('Solution validated and found correct')
    else:
        print('Incorrect solution')


def main():
    file_name = sys.argv[1]
    orig_data = np.genfromtxt("./../../data/linal/" + file_name, delimiter=",")
    print("Original appended matrix: \n{}".format(orig_data))
    print("Appended matrix shape: {}".format(orig_data.shape))
    data = orig_data.copy()
    row_echleon_data = gaussian_elimination(data)
    print("row echleon form: \n{}".format(row_echleon_data))
    solution_vector = back_substitution(row_echleon_data)
    print("solution vector: {}".format(solution_vector))
    validate_solution(orig_data, solution_vector)


if __name__ == "__main__":
    main()
import numpy as np
import sys

# LU factorization algorithm
# 1. Want to solve Ax = b ( A is a matrix, x and b are vectors. This is how you represent a system of
# linear equations using matrix and vectors )
# 2. Find lower triangular matrix L and upper triangular matrix U such that A = LU (this is LU factorization)
# 3. Substitute LUx = b
# 4. Matrix multiplication is associative, this L(Ux) = b. Let's call multiplication of U and x to be z
# Note that Ux is of the form 2x+4y-2z = -10
#                               -10y+10z = 40
#                                   -8z = -16
# 5. We first want to solve Lz = y. This is what constitutes the forward substitution algorithm. We get the z vector
# as the solution
# 6. Solve Ux = z. This is what the back substitution algorithm does


def gaussian_elimination(data):
    # data is the appended matrix. Extract from it the matrix that represent the LHS side of equations
    l_data = data[:, 0:-1]
    n_rows, n_cols = l_data.shape
    lower_triangular = np.eye(n_rows, n_cols)
    row_pivots = {}
    i = 0
    j = 0
    while i < n_rows-1 and j < n_cols:
        # perform gaussian elimination to render an upper triangular matrix with the elements below the diagonal
        # elements in each column containing the multipliers
        alpha11 = l_data[i][j]
        # If alpha11 is 0, then row pivoting needs to be done using permutation matrices to prevent divide by zero error
        # This is done by swapping row i with the row next first row that has a non zero entry in column j
        if alpha11 == 0:
            first_nonzero_index = get_swap_index(i, j, l_data)
            print("row pivot i={}, first_nonzero_index > i = {}".format(i, first_nonzero_index))
            row_pivots.update({i: first_nonzero_index})
            # now do a row swap between i and first_nonzero_index
            l_data[[i, first_nonzero_index]] = l_data[[first_nonzero_index, i]]
            # lower_triangular[[i, first_nonzero_index]] = lower_triangular[[first_nonzero_index, i]]
            alpha11 = l_data[i][j]
        a21 = l_data[i + 1:, j]
        A22 = l_data[i + 1:, j + 1:]
        a12T = l_data[i, j + 1:]
        # l21 is the multiplier vector in the gauss transform which we store in the original matrix below the
        # 1 in the diagonal in the current column
        l21 = a21 / alpha11
        # Elements below the diagonal element in the current column become all zero after multiplication with the
        # gauss transform
        l_data[i + 1:, j] = np.zeros(l21.shape)
        # Store the gauss transform in the lower triangular matrix
        lower_triangular[i+1:, j] = l21
        A22 = A22 - np.outer(l21, a12T)
        l_data[i + 1:, j + 1:] = A22
        # next iteration
        i += 1
        j += 1
    return lower_triangular, l_data, row_pivots


def get_swap_index(i, j, l_data):
    """
    Returns the first index value ( > i ) in column j that is non zero in case a zero value is encountered
    in a diagonal element that can lead to a divide by zero error when calculating the multipliers for
    the gauss transform
    :param i: row index
    :param j: column index
    :param l_data: LHS of the appended matrix
    :return: first index value ( > i ) in column j that is non zero
    """
    list_col_j = l_data[0:, j].tolist()
    list_col_j_index = list(range(len(list_col_j)))
    first_nonzero_index = [index for value, index in tuple(zip(list_col_j, list_col_j_index))
                           if value != 0 and index > i][0]
    return first_nonzero_index


def fwd_substitution(lower_triangular, r_data, row_pivots):
    # perform forward substitution on the rightmost column in the appended matrix
    n_rows, n_cols = lower_triangular.shape
    i = j = 0
    while i < n_rows and j < n_cols:
        # check if during LU factorization a row swap was done on current row, if yes do the same on r_data
        if i in row_pivots:
            swap_index = row_pivots.get(i)
            r_data[[i, swap_index]] = r_data[[swap_index, i]]
        beta1 = r_data[i]
        b2 = r_data[i + 1:]
        b2 = b2 - (beta1 * lower_triangular[i+1:, j])
        r_data[i + 1:] = b2
        i += 1
        j += 1
    return r_data


def back_substitution(upper_triangular, r_data):
    # we will march from the bottom up partitioning the matrix
    i = j = 0
    reverse_ut = upper_triangular[:: -1]
    reverse_r_data = r_data[::-1]
    u_BR = reverse_ut[i:0, j:0]
    n_rows, n_cols = reverse_ut.shape
    while i < n_rows and j < n_cols:
        gamma11 = reverse_ut[i, -j-1]
        # since we are marching bottom, we need to reverse the array representing rhs of linear eq system.
        b2 = reverse_r_data[0:i][::-1]
        beta1 = reverse_r_data[i]
        u12T = reverse_ut[i, -1:-j-1:-1][::-1]
        beta1 = beta1 - np.dot(u12T, b2)
        reverse_r_data[i] = beta1 / gamma11
        i += 1
        j += 1
    return r_data


def validate_solution(data, solution_vector):
    # extract the left part from the appended matrix.
    data_left = data[:, 0:-1]
    # extract the right part ( the one after the equals to in system of linear eq ) from the appended matrix
    # as a vector
    data_right = data[:, -1]
    solved_vector = np.dot(data_left, solution_vector)
    print("\nsolved vector: {}".format(solved_vector))
    if np.array_equal(data_right, solved_vector):
        print('solution validated and found correct')
    else:
        print('incorrect solution')


def main():
    file_name = sys.argv[1]
    orig_data = np.genfromtxt("./../../data/linal/" + file_name, delimiter=",")
    print("Original appended matrix: \n{}".format(orig_data))
    print("Appended matrix shape: {}".format(orig_data.shape))
    data = orig_data.copy()
    r_data = data[:, -1]
    lower_triangular, upper_triangular, row_pivots = gaussian_elimination(data)
    print("After LU factorization:\n\nlower triangular matrix: \n{}".format(lower_triangular))
    print("upper triangular matrix: \n{}".format(upper_triangular))
    print("\nGoing to solve Lz = b using forward substitution")
    z = fwd_substitution(lower_triangular, r_data, row_pivots)
    print("z = {}".format(z))
    print("\nGoing to solve Ux = z using back substitution")
    solution_vector = back_substitution(upper_triangular, z)
    print("solution vector: {}".format(solution_vector))
    validate_solution(orig_data, solution_vector)


if __name__ == "__main__":
    main()
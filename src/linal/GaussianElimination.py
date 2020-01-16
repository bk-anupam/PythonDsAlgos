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
    i = 0
    j = 0
    while i < n_rows-1 and j < n_cols:
        # perform gaussian elimination to render an upper triangular matrix with the elements below the diagonal
        # elements in each column containing the multipliers
        alpha11 = l_data[i][j]
        a21 = l_data[i+1:, j]
        A22 = l_data[i+1:, j+1:]
        a12T = l_data[i, j+1:]
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
    return lower_triangular, l_data


def fwd_substitution(lower_triangular, r_data):
    # perform forward substitution on the rightmost column in the appended matrix
    n_rows, n_cols = lower_triangular.shape
    i = j = 0
    while i < n_rows and j < n_cols:
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
    lower_triangular, upper_triangular = gaussian_elimination(data)
    print("After LU factorization:\n\nlower triangular matrix: \n{}".format(lower_triangular))
    print("upper triangular matrix: \n{}".format(upper_triangular))
    print("\nGoing to solve Lz = b using forward substitution")
    z = fwd_substitution(lower_triangular, r_data)
    print("z = {}".format(z))
    print("\nGoing to solve Ux = z using back substitution")
    solution_vector = back_substitution(upper_triangular, z)
    print("solution vector: {}".format(solution_vector))
    validate_solution(orig_data, solution_vector)


if __name__ == "__main__":
    main()
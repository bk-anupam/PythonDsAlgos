import sys


# Bottom up approach by filling up a 2-D array
def lcs_table(strx, stry):
    lcs_array = [[0 for row in range(len(stry)+1)] for col in range(len(strx)+1)]
    for x in range(1, len(strx)+1):
        for y in range(1, len(stry)+1):
            # case 1: the last character for both string matches
            if strx[x-1] == stry[y-1]:
                lcs_array[x][y] = lcs_array[x-1][y-1] + 1
            else:
                lcs_array[x][y] = max(lcs_array[x][y-1], lcs_array[x-1][y])
    return lcs_array


# From the table, backtrack to retrieve one of the LCSes
def backtrack(lcs_array, str_x, str_y, i, j):
    if i == 0 or j == 0:
        return ""
    if str_x[i-1] == str_y[j-1]:
        return backtrack(lcs_array, str_x, str_y, i-1, j-1) + str_x[i-1]
    if lcs_array[i-1][j] > lcs_array[i][j-1]:
        return backtrack(lcs_array, str_x, str_y, i-1, j)
    else:
        return backtrack(lcs_array, str_x, str_y, i, j-1)


def backtrack_all(lcs_array, str_x, str_y, i, j):
    if i == 0 or j == 0:
        return set([""])
    elif str_x[i-1] == str_y[j-1]:
        return set([lcs+str_x[i-1] for lcs in backtrack_all(lcs_array, str_x, str_y, i-1, j-1)])
    else:
        all_lcs = set()
        if lcs_array[i-1][j] >= lcs_array[i][j-1]:
            all_lcs.update(backtrack_all(lcs_array, str_x, str_y, i-1, j))
        if lcs_array[i][j-1] >= lcs_array[i-1][j]:
            all_lcs.update(backtrack_all(lcs_array, str_x, str_y, i, j-1))
        return all_lcs


def main():
    if len(sys.argv) == 1:
        raise Exception("No arguments were provided. Provide the two strings to compare as argument")
    str_x = sys.argv[1]
    str_y = sys.argv[2]
    lcs_array = lcs_table(str_x, str_y)
    common_string_len = lcs_array[len(str_x)][len(str_y)]
    lcs = backtrack(lcs_array, str_x, str_y, len(str_x), len(str_y))
    all_lcs = backtrack_all(lcs_array, str_x, str_y, len(str_x), len(str_y))
    print("Length of common subsequence: {}".format(common_string_len))
    print('one of the lcs: ' + lcs)
    # test strings: AATCC, ACACG
    print(all_lcs)


if __name__ == "__main__":
    main()
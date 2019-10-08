import sys


# Bottom up approach by filling up a 2-D array
def lcs_length(strx, stry):
    lcs_array = [[0 for row in range(len(stry)+1)] for col in range(len(strx)+1)]
    for x in range(1, len(strx)+1):
        for y in range(1, len(stry)+1):
            # case 1: the last character for both string matches
            if strx[x-1] == stry[y-1]:
                lcs_array[x][y] = lcs_array[x-1][y-1] + 1
            else:
                lcs_array[x][y] = max(lcs_array[x][y-1], lcs_array[x-1][y])
    val = lcs_array[len(strx)][len(stry)]
    return val


def main():
    if len(sys.argv) == 1:
        raise Exception("No arguments were provided. Provide the two strings to compare as argument")
    common_string_len = lcs_length(sys.argv[1], sys.argv[2])
    print("Length of common subsequence: {}".format(common_string_len))


if __name__ == "__main__":
    main()
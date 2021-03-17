# N Queens problem (https://developers.google.com/optimization/cp/queens)

diag_indices_cache = {}


def get_diagonal_indices(i, j, N):
    key = f'({i},{j})'
    if key in diag_indices_cache:
        return diag_indices_cache[key]

    diag_indices = [(i, j)]
    temp_row_index = i
    temp_col_index = j
    while temp_row_index < N-1 and temp_col_index < N-1:
        temp_row_index += 1
        temp_col_index += 1
        diag_indices.append((temp_row_index, temp_col_index))
    temp_row_index = i
    temp_col_index = j
    while temp_row_index > 0 and temp_col_index > 0:
        temp_row_index -= 1
        temp_col_index -= 1
        diag_indices.append((temp_row_index, temp_col_index))
    temp_row_index = i
    temp_col_index = j
    while temp_row_index < N-1 and temp_col_index > 0:
        temp_row_index += 1
        temp_col_index -= 1
        diag_indices.append((temp_row_index, temp_col_index))
    temp_row_index = i
    temp_col_index = j
    while temp_row_index > 0 and temp_col_index < N-1:
        temp_row_index -= 1
        temp_col_index += 1
        diag_indices.append((temp_row_index, temp_col_index))
    diag_indices_cache[key] = diag_indices
    return diag_indices


def is_cell_attacked(board, row_i, col_i, N):
    # Criteria 1: A queen already placed in row_i or col_i
    for col_index in range(N):
        if board[row_i][col_index] == 1:
            return True
    for row_index in range(N):
        if board[row_index][col_i] == 1:
            return True
    # Criteria 2: In the diagonal cells for (row_i, col_i) a queen has been already placed
    q_diag_indices = get_diagonal_indices(row_i, col_i, N)
    for index_pair in q_diag_indices:
        if board[index_pair[0]][index_pair[1]] == 1:
            return True
    return False


def solve_N_queens(board, N, rows_placed, sol_list):
    if rows_placed == N:
        sol_list.append(board)
        return
    for col_index in range(N):
        if not is_cell_attacked(board, rows_placed, col_index, N):
            board[rows_placed][col_index] = 1
            solve_N_queens(board, N, rows_placed + 1, sol_list)
            board[rows_placed][col_index] = 0
    return

def backtrack(N, board, curr_row, queen_stack):
    stack_full = False
    if len(queen_stack) == N:
        stack_full = True
    curr_col = queen_stack.pop()
    if not stack_full:
        curr_row -= 1
    # If you have reached the last column of first row, you have explored all possibilities
    if curr_col >= N-1 and curr_row == 0:
        return -1, -1
    board[curr_row][curr_col] = 0
    while curr_col == N - 1 and curr_row > 0:
        if len(queen_stack) > 0:
            curr_col = queen_stack.pop()
            curr_row -= 1
            board[curr_row][curr_col] = 0
    curr_col += 1
    return curr_col, curr_row

def solve_N_queens_stack(board, N, curr_row, curr_col, sol_list):
    queen_stack = []
    while curr_col != -1:
        for col_index in range(curr_col, N, 1):
            if not is_cell_attacked(board, curr_row, col_index, N):
                board[curr_row][col_index] = 1
                queen_stack.append(col_index)
                if curr_row < N-1:
                    curr_row += 1
                    curr_col = 0
                break
            # Once you have reached the last column of the current row, check if a valid queen pos has been found
            if col_index == N-1:
                try:
                    queen_stack[curr_row]
                except IndexError:
                    curr_col, curr_row = backtrack(N, board, curr_row, queen_stack)

        if len(queen_stack) == N:
            sol_list.append(board)
            curr_col, curr_row = backtrack(N, board, curr_row, queen_stack)

N = 8
board = [[0 for col in range(N)]for row in range(N)]
sol_list = []
#solve_N_queens(board, N, 0, sol_list)
solve_N_queens_stack(board, N, 0, 0, sol_list)
print(f"Number of solutions = {len(sol_list)}")

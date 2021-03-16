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


def is_attacked(queens_placed, p_row_index, p_col_index, N):
    for q_row_index, q_col_index in queens_placed:
        # The next queen can't be placed in the same row or column as an existing queen
        if q_row_index == p_row_index or q_col_index == p_col_index:
            return True
        # Two diagonals can possibly pass thru each board cell. The next queen can't be placed
        # in any of the cells of the two diagonals that pass thru an existing queen
        q_diag_indices = get_diagonal_indices(q_row_index, q_col_index, N)
        for index_pair in q_diag_indices:
            if index_pair[0] == p_row_index and index_pair[1] == p_col_index:
                return True
    return False


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

N = 8
board = [[0 for col in range(N)]for row in range(N)]
sol_list = []
solve_N_queens(board, N, 0, sol_list)
print(f"Number of solutions = {len(sol_list)}")

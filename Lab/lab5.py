def forward_check(matrix, row, col, domains): #foward checking
    for i in range(4):
        for j in range(4):
            if matrix[i][j] == 0:  # nepopunjeno
                domains[i][j] = [ num for num in domains[i][j] if is_valid(matrix, i, j, num) ]
                if not domains[i][j]:  # ako domen postane prazan
                    return False
    return True

def is_valid(matrix, row, col, num):
    for i in range(4):
        if matrix[row][i] == num or matrix[i][col] == num:
            return False
    return True

def lcv_heuristic(domains, row, col): # sort po least constraining value
    return sorted(domains[row][col], key = lambda val: sum( val in domains[i][j] for i in range(4) for j in range(4) if i != row or j != col ))

def solve(matrix, domains, row = 0, col = 0):
    if row == 4:
        return True

    next_row, next_col = (row, col + 1) if col < 3 else (row + 1, 0)

    if matrix[row][col] != 0: # ako je puna idemo dalje
        return solve(matrix, domains, next_row, next_col)

    for num in lcv_heuristic(domains, row, col):
        if is_valid(matrix, row, col, num):
            matrix[row][col] = num

            saved_domains = [row[:] for row in domains]
            domains[row][col] = [num] # azurira domen

            if forward_check(matrix, row, col, domains) and solve(matrix, domains, next_row, next_col):
                return True

            # prethodno stanje
            matrix[row][col] = 0
            domains = saved_domains

    return False

# init
matrix = [[0 for _ in range(4)] for _ in range(4)]
domains = [ [[1, 2, 3, 4] for _ in range(4)] for _ in range(4) ]

if solve(matrix, domains):
    for row in matrix:
        print(row)
else:
    print("nema resenja")

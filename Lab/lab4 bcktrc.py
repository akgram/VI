
N = 5

figures = [
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],  # Zelena
    [(0, 0), (1, 0), (2, 0), (1, 1), (2, 1)],  # Plava
    [(0, 0), (0, 1), (1, 0), (2, 0), (2, 1)],  # Narandzasta
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 2)],  # Crvena
    [(1, 0), (1, 1), (2, 1), (2, 2), (2, 3)],  # Zuta
]

def rotate_figure(figure): # za 90
    return [(-y, x) for x, y in figure]

def generate_rotations(figures):
    all_rotations = []
    for figure in figures:
        rotations = []
        current = figure
        for _ in range(4):  # do 4 rotacije
            rotations.append(current)
            current = rotate_figure(current)
        all_rotations.append(rotations)
    return all_rotations

def is_valid(board, figure, x, y):
    for dx, dy in figure:
        nx, ny = x + dx, y + dy
        if nx < 0 or nx >= N or ny < 0 or ny >= N or board[nx][ny] != 0:
            return False
    return True

def place_figure(board, figure, x, y, figure_id):
    for dx, dy in figure:
        board[x + dx][y + dy] = figure_id

def remove_figure(board, figure, x, y):
    for dx, dy in figure:
        board[x + dx][y + dy] = 0

def solve(board, rotations, figure_index):
    if figure_index == len(rotations):
        return True

    for rotation in rotations[figure_index]:
        for x in range(N):
            for y in range(N):
                if is_valid(board, rotation, x, y):
                    place_figure(board, rotation, x, y, figure_index + 1)

                    if solve(board, rotations, figure_index + 1):
                        return True

                    remove_figure(board, rotation, x, y)

    return False

def main():
    board = [[0] * N for _ in range(N)]
    rotations = generate_rotations(figures)

    if solve(board, rotations, 0):
        print("Resenje pronadjeno:")
        for row in board:
            print(row)
    else:
        print("Nema resenja.")

main()

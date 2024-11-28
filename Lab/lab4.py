def a_star(start, tabla, figures):
    found_end = False
    open_set = set() # svi
    closed_set = set() # obradjeni cvorovi
    g = {}  # cena puta
    prev_nodes = {}
    g[start] = 0
    prev_nodes[start] = None
    open_set.add(tuple(start, ))

    while len(open_set) > 0 and not found_end:
        node = None
        for next_node in open_set:
            if node is None or g[next_node] + h_function(next_node) < g[node] + h_function(node):
                node = next_node
        
        if all_figures_placed(tabla, figures):
            found_end = True
            break

        for destination in get_valid_moves(node, tabla, figures):
            if destination not in open_set and destination not in closed_set:
                open_set.add(destination)
                prev_nodes[destination] = node
                g[destination] = g[node] + 1
            else:
                if g[destination] > g[node] + 1:
                    g[destination] = g[node] + 1
                    prev_nodes[destination] = node
                if destination in closed_set:
                    closed_set.remove(destination)
                    open_set.add(destination)
        
        open_set.remove(node)
        closed_set.add(node)

    path = []
    if found_end:
        while prev_nodes[node] is not None:
            path.append(node)
            node = prev_nodes[node]
        path.append(start)
        path.reverse()
    return path


def h_function(tabla, figures):
    unplaced_count = 0
    for figure in figures:
        if not all_figures_placed(figure, tabla):
            unplaced_count += 1
    return unplaced_count

def get_valid_moves(node, tabla, figures):
    valid_moves = []
    for figure in figures:
        if can_place_figure(node, figure, tabla):
            valid_moves.append(node)
    return valid_moves


def can_place_figure(node, figure, tabla):
    for position in figure:
        if not valid_move(position, tabla):
            return False
    return True


def valid_move(node, tabla):
    if node[0] < 0 or node[0] >= 5 or node[1] < 0 or node[1] >= 5:
        return False
    if tabla[node[0]][node[1]] != 0:
        return False
    return True

def all_figures_placed(tabla, figures):
    for figure in figures:
        for position in figure:
            if tabla[position[0]][position[1]] == 0:
                return False
    return True

tabla = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

figures = [
    [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)],  # zelena
    [(0, 3), (1, 3), (2, 3), (2, 4), (3, 3)],  # plava
    [(3, 0), (3, 1), (4, 0), (4, 1), (4, 2)],  # narandzasta
    [(1, 4), (2, 4), (2, 5), (3, 4), (3, 5)],  # crvena
    [(0, 2), (1, 2), (2, 2), (2, 3), (3, 2)]   # zuta
]

start = (0, 0)

path = a_star(start, tabla, figures)
print(path)

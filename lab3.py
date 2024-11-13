#17. Napisati funkciju koja na osnovu zadatog težinskog neusmerenog grafa i zadatog (ciljnog) čvora G
#formira neusmereni težinski graf sa heuristikom. Heuristika proizvoljnog čvora C se određuje kao
#dužina puta od čvora C do čvora G. 



#from multiprocessing import process
import queue


def hill_climbing_search(graph, start, end):
    if start is end:
        path = []
        path.append(start)
        return path
    stack_nodes = queue.LifoQueue(len(graph)) #LifoQueue
    visited = set()
    prev_nodes = dict()
    prev_nodes[start] = None
    visited.add(start)
    stack_nodes.put(start)
    found_dest = False

    while (not found_dest) and (not stack_nodes.empty()):
        node = stack_nodes.get()
        #process(node)
        destinations = []
        for dest in graph[node][1]:
            element = (graph[dest][0], dest)
            destinations.append(element)
        for dest_heur in sorted(destinations, reverse=True):
            if dest_heur[1] not in visited:
                prev_nodes[dest_heur[1]] = node
                if dest_heur[1] is end:
                    found_dest = True
                    break
                visited.add(dest_heur[1])
                stack_nodes.put(dest_heur[1])

    path = []
    if found_dest:
        path.append(end)
        prev = prev_nodes[end]
        while prev is not None:
            path.append(prev)
            prev = prev_nodes[prev]
        path.reverse()
    return path

graph_simple = {
'A' : (4, ['B','C']),
'B' : (3, ['D', 'E']),
'C' : (2, ['F', 'G']),
'D' : (9, ['H']),
'E' : (2, ['G', 'I']),
'F' : (1, ['J']),
'G' : (1, ['J']),
'H' : (9, []),
'I' : (1, ['J']),
'J' : (0, [])
}

path = hill_climbing_search(graph_simple, 'A', 'J')
print(path)
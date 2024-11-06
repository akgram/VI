
graph_simple = {
'A' : (9, ['B','C']),
'B' : (6, ['D', 'E']),
'C' : (7, ['F', 'G']),
'D' : (4, ['H']),
'E' : (8, ['G', 'I']),
'F' : (3, ['J']),
'G' : (4, ['J']),
'H' : (4, []),
'I' : (3, ['J']),
'J' : (0, [])
}
path = hill_climbing_search(graph, start, end) # planinarenje sort sledbenike po heuristici? (vrsta trazenja po dubini)

path = best_first_search(graph, start, end) # sort prema svim cvorovima po heuristici (vrsta trazenja po dubini)


path = breadth_first_search(graph, start, end) # po sirini, koristimo red

path = depth_first_search(graph, start, end) # po dubini, koristimo stack





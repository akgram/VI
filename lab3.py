#9. Napisati funkciju koja određuje broj čvorova do kojih može da se dođe od zadatog čvora, tako da
#je dužina puta do čvora jednaka zadatoj vrednosti. Obići samo neophodne čvorove. 

from collections import deque

def dist(graph, start, target_dist):
    queue = deque([(start, 0)])
    visited = set()
    count = 0
    visited.add(start)
    #queue.put(start)
    
    while queue:
        node, distance = queue.popleft()
        
        if distance == target_dist:
            count += 1
            continue
        
        for neighbor in graph[node]:
            new_distance = distance + 1
            if neighbor not in visited and new_distance <= target_dist:
                visited.add(neighbor)
                queue.append((neighbor, new_distance))
    
    return count

graph = {
    1: {2: 2, 3: 1},
    2: {1: 3, 4: 2},
    3: {1: 1, 4: 4},
    4: {2: 5, 3: 3, 5: 1},
    5: {4: 1}
}
result = dist(graph, 4, 2)
print(result)

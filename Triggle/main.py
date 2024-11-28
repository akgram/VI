
def dimTable():
    print("Unesite dimenziju table: ", end="")
    n = input()

    while(n.isdigit() == False):
        print("GRESKA! Unesite BROJ: ")
        n = input()

    n = int(n)
    return n



def graf(n):

    graph = {
            'A': (n, [])
        }
    i = 1
    while(i < n): # gornja polovina i sredina
        br = n + i
        graph[chr(65 + i)] = (br, [])
        i += 1

    j = 1
    while(j < n): # donja polovina
        br = n + i - j - 1
        graph[chr(65 + j - 1 + n)] = (br, [])
        j += 1

    return graph
    
def startState(graph, n): # pocetno stanje przna tabla
    for x in graph:
        a = int(graph[x][0])
        x_num = (ord(x) - ord('A'))
        if(x_num < n):
            print(x, " " * (a - 2 * x_num - 1) + "● " * a)
        else:
            print(x, " " * (x_num % n + 1) + "● " * a)



n = dimTable()
startState(graf(n), n)
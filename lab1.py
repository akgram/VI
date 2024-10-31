from functools import reduce
from itertools import chain, combinations, combinations_with_replacement, compress, count, cycle, dropwhile, filterfalse, groupby, islice, pairwise, permutations, product, repeat, starmap, takewhile, tee, zip_longest


def func1(el, n, list):
    new_list = list[:n] + [el] + list[n:]
    return new_list

list0 = [1, "lab1", True, "ne znam"]
print(func1(11, 2, list0))

###############################

def func3(list):
    i = 0
    for x in list:
        if x != []:
            i += 1
    print(i)

list1 = [1, "lab1", True, "ne znam", 213, "nesto"]
func3(list1)

###############################

def poredak(list1, list2):
    a = len(list1) - len(list2)
    if a > 0:
        list2 += [0] * a
    elif a < 0:
        list1 += [0] * a

    rez = list(map(lambda x, y: (x, y, 'Jeste' if y == 2 * x else 'Nije'), list1, list2))
    return rez

l1 = [1, 7, 2, 4]
l2 = [2, 5, 2]
print(l1)
print(l2)
print(poredak(l1, l2))
##########################

def numlista(list1):
    rez = list(filter(lambda x: type(x) == int or type(x) == float, list1))
    return rez

l3 = [2, 5, "aca", True, 'lavaca', 1.1]
print(numlista(l3))

#########################

def factorial(n):
    if n == 0:
        return 1
    else:
        return factorial(n-1) * n
    
print(factorial(3))

print((lambda x: x ** 2 if 0 == 0 else "ne")(5))

#########################

print(min((2, 4), (3, 8), (1, 9), key = lambda x: x[1])) # min po 2. koordinati x[1]

print(max((2, 4), (3, 8), (1, 9), key = lambda x: x[0])) # max po 1. koordinati x[0]

print(sorted([(2, 4), (3, 8), (1, 5)], key = lambda x: x[1])) # rastuci

print(sorted([1, 2, 3, 4, 5], reverse = True)) # opadajuci

#########################

a = list(zip(l1, l2))
print(a)

########################

print(reduce(lambda x, y: x + y, range(1, 11)))

########################

#print(list(count(11, 2))) u beskonacno ide

#print(list(cycle([1, 2, 3]))) u beskonacno

print(list(repeat(11, 5)))

print(list(chain(["aca", "lavaca"])))

print(list(compress("acalavaca", [0, 0, 0, 1, 1, 1, 0, 0, 0])))

print(list(dropwhile(lambda x: x < 2, [1, 2, 3, 7, 'aca'])))

print(list(filterfalse(lambda x: x < 3, [1, 2, 3, 7])))

for k, g in groupby('AAAABBBCCDAABBB'):
    print((k, len(list(g))))

print(list(islice("ABCDEF", 1, 4, 2))) # start, stop, step

print(list(pairwise("ACAB")))

print(list(starmap(lambda x, y: x ** y, [(2, 5), (3, 2)])))

print(list(takewhile(lambda x: x < 20, count(10, 3))))

for x in list(tee(range(1, 10), 2)): # Vraća n ponavljanja prosleđene kolekcije
    print(list(x))

print(list(zip_longest('ABCD', 'xy', fillvalue='/')))

print(list(product("AB", "AB"))) # svaki sa svakim

print(list(permutations("ABC", 2))) # per duzine 2

print(list(combinations("ABCD", 2))) # komb duzine 2

print(list(combinations_with_replacement('ABC', 2))) # komb sa ponavljanjem duzine 2

####################
match 'A':
    case ('A' | 'B' | 'C') as slovo:
        print(slovo)
    case 'a':
        print("Uslov")
    case ('a', _):
        print("Novi")
    case _:
        print("Default") 

lista1 = [1, 7, 2, 4, 5]

def parni(lista):
    dict1 = { 
        'Parni': [x for x in lista if x % 2 == 0],
        'Neparni': [x for x in lista if x % 2 != 0] 
    }
    print(dict1)

parni(lista1)
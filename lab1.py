def func1(el, n, list):
    new_list = list[:n] + [el] + list[n:]
    return new_list

list = [1, "lab1", True, "ne znam"]
print(func1(11, 2, list))

###############################

def func3(list):
    i = 0
    for x in list:
        if x != []:
            i += 1
    print(i)

list1 = [1, "lab1", True, "ne znam", 213, "nesto"]
func3(list1)
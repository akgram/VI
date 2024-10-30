
from itertools import accumulate, starmap


print(list(starmap(lambda x, y: x ** y, [(2, 5), (2, 3)])))

#iter kad prodje korz iteraciju pokazivac ostaje na kraju liste pa ce 
#slecedi prolaz da vrati praznu listu... moze da se resi sa tee()

print([x for x in range(1, 11)])

a = 2
b = 2
print(a or b)
#################
tuple = ('aca', 2)
print(tuple)
#tuple[1] = 3 # baca gresku, tuple se ne moze menjati
print(tuple)
##################
dict = {
    "marka": "Mercedes",
    "model": "E220"
}

print(dict.items())
###################
set = { "aca", "lavaca", 11, 11, 11} # samo jedno 11 pise jer set ne dozvoljava duplikate
set2 = { "gas", "night", 1, 11}
set.add(2)
set.remove(11)
print(set)
print("aca" in set)
set.update(set2)
print(set)
#################
if a > b:
    print("nista")
elif a == b:
    print("dadada")
##################
list1 = ["sever", "jug", 1]
for x in list1:
    if x == "jug":
        continue
    print(x)
else:      # izvrsava se posle for sem ako je for zaustevljen sa break
    print("gotovo") 
################
for x in range(7, 11):
    print(x)
################
i = 1
while i < 3:
    print("gasgas")
    i += 1

################

def funkcija(a):
    print(a + 2)

funkcija(3)

################

def func(*a, **k):
    print(a)
    print(k)

func("ovo", "je", 1, "recenica", key = "value", ki = "velj ju")

f = input("unesi broj: ")
print(f)


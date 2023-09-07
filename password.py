#password creator(most likely not secure)
import random


Pass = ""
test = random.randint(20, 30)
bool = True

for i in range(0,test):
    while(bool):
        num =random.randint(33, 122)
        if num == 34|39|58|59|60|61|62|96:
            num = random.randint(33, 122)

        else:
            break
    
    Pass = Pass + chr(num)
    print(Pass)



            



    
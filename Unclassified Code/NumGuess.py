import random
global newNum
newNum = -1

num = random.randint(0,600)


while(newNum  != num):
    print("enter in a guess")
    string = input()

    newNum = int(string)

    if(newNum == num):
        print("------------------you guessed correctly------------------")
        break
    elif (newNum > num-5) and (newNum < num+5):
        print("very hot")
    elif (newNum > num-10) and (newNum < num+10):
        print("Hotter")
    elif (newNum > num-25) and (newNum < num+25):
        print("warmer")
    elif (newNum > num-50) and (newNum < num+50):
        print("cold")   
    elif (newNum > num-100) and (newNum < num+100):
        print("freezing")
    else:
        print("subzero")

import random
def main():
    print ("Guess a number")
    randNumber = random.randint(1,100)
    myflag = False
    while not myflag:
        userGuess = int(input("your Guess:"))
        if userGuess == randNumber:
            print ("You Got it!")
            myflag = True
        elif userGuess > randNumber:
            print ("Guess lower")
        else:
            print ("guess higher")
main()

v=input('Enter value:')
try:
    v=int(v)
    if (v<0 or v>100):
        print ("Please enter a value between 0 and 100")
    v= {
        90<=v: "A",
        70<=v<90: "B",
        50<=v<70: "C",
        35<=v<50: "D",
        0<v<35: "E"
        }
        
    grade= v.get(True, "Bad Score")
    print (grade)
    #elif v<35:
        #print("Grade E", "Marks", v, "/100")
    #elif (v>=35 and v<50):
        #print("Grade D", "Marks", v, "/100")
    #elif (v>=50 and v<70):
        #print("Grade C", "Marks", v, "/100")
    #elif (v>=70 and v<90):
        #print("Grade B", "Marks", v, "/100")
    #elif (v>=90 and v<100):
        #print("Grade A", "Marks", v, "/100")
except:
    print("Please enter a numeric input")
print ("Good luck!")

try:
    Hours,Rate = map(float, input().split())
    hours = float (Hours)
    #inp = input('Enter pay rate:')
    rate = float (Rate)
except:
    print ('Error, please enter numeric input')
    quit()

print (hours, rate)
if hours <= 40:
    pay = hours * rate
else:
    pay = rate * 40 + (rate * 1.5 * (hours - 40))
print (pay)    

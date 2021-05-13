import datetime
from time import sleep
from math import remainder

print("{}-{}-{}".format(datetime.date.today().day, datetime.date.today().month, datetime.date.today().year))

print(datetime.datetime.now())

datetime0=datetime.datetime.now()
while True:
    elapsedtime=datetime.datetime.now()-datetime0
    # print(elapsedtime.seconds+elapsedtime.microseconds/100000.0, end="\r")
    # sleep(2)
    if remainder(elapsedtime.seconds+elapsedtime.microseconds/100000.0, 3)<=0.0001 and remainder(elapsedtime.seconds+elapsedtime.microseconds/100000.0, 3)>=-0.0001:
        print("Hi tandu!")
        # datetime0=elapsedtime
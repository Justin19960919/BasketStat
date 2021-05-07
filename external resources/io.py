# Input output
import datetime

def gamelog(path, msg):

    with open(path, 'a') as f:
        f.write(msg)

print("testing for logger")

while(1):
    print("Pass in a message: ")
    msg = input()
    gamelog("log/test.txt", msg)
    

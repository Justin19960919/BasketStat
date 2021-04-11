# Input output
import datetime

def gamelog(path, msg):
    file = open(path, "a")
    msg_time = datetime.datetime.now()
    msg_time = msg_time.strftime("%m/%d/%Y, %H:%M:%S")
    file.write(msg_time)
    file.write(" ")
    file.write(msg)
    file.write("\n")
    file.close()

print("testing for logger")

while(1):
    print("Pass in a message: ")
    msg = input()
    gamelog("test.txt", msg)
    

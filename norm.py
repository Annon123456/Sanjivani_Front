import threading 
def fun():         # user defined function which adds +10 to given number
    
    print ("Hey u called me")
    

start_time = threading.Timer(3,fun)
start_time.start()
print ("End of the code")
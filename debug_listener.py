#!/usr/bin/env python

import socket, threading
import ConfigParser


config = ConfigParser.ConfigParser()
config.readfp(open('defaults.cfg'))

HOST = config.get("log_generator",'HOST')
PORT = config.getint("log_generator",'PORT')


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(4)
clients = [] #list of clients connected
lock = threading.Lock()


class chatServer(threading.Thread):
    def __init__(self, (socket,address)):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address= address

    def run(self):
        lock.acquire()
        clients.append(self)
        lock.release()
        print '%s:%s connected.' % self.address
        try:
            while True:
                data = self.socket.recv(1024)
                print data
                if not data:
                    break
                for c in clients:
                    c.socket.send(data)
        except:
            self.socket.close()
            print '%s:%s disconnected.' % self.address
            lock.acquire()
            clients.remove(self)
            lock.release()

try:
    while True: # wait for socket to connect
        # send socket to chatserver and start monitoring
            chatServer(s.accept()).start()
except KeyboardInterrupt:
    print "Shutting down gracefully"
    exit()

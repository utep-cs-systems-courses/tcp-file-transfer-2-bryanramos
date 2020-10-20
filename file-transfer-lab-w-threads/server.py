#! /usr/bin/env python3

# Author: Bryan Ramos
# Course: Theory of Operating Systems (OS)
# Instructors: Eric Freudenthal and David Pruitt
# Assignment: Lab 2 - TCP File Transfer w/ Threads

import os, socket, sys, threading, time

sys.path.append("../lib") # for params
import params
from threading import Thread
from encapFramedSock import EncapFramedSock

PATH = "./Receive"
HOST = "127.0.0.1"

switchesVarDefaults = (
    (('1', '--listenPort'), 'listenPort', 50001),
    (('?', '--usage'), 'usage', False),
    (('d', '--debug'), 'debug', False),
)

parameterMap = params.parseParams(switchesVarDefaults)
listenPort, debug = parameterMap['listenPort'], parameterMap['debug']

if parameterMap['usage']:
    params.usage()

bindAddress = (HOST, listenPort)

# creating listening socket
listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listenSocket.bind(bindAddress)

listenSocket.listen(10) # 10 connections
print("Listening on: ", bindAddress)

# create lock
lock = threading.Lock()

# following guidance from class lecture and framedThreadServer.py demo
class Server(Thread):

    def __init__(self, sockAddress):
        Thread.__init__(self)
        self.sock, self.address = sockAddress
        self.fsock = EncapFramedSock(sockAddress)

    def run(self):
        print("new thread handling connection from", self.address)
        while 1:
            try:
                fileName, contents = self.fsock.receive(debug)
            except:
                print("Error: File transfer was not successful!")
                self.fsock.sendStatus(0, debug)
                self.fsock.close()
                sys.exit(1)

            if debug:
                print("Received", contents)

            # client closed = data not received
            if fileName is None or contents is None:
                print ("Client ", self.address, " has disconnected")
                sys.exit(0)
            
            lock.acquire()
            if debug:
                time.sleep(5)
            
            # write file
            fileName = fileName.decode()
            self.writeFile(fileName, contents)

            # return message of success
            self.fsock.sendStatus(1, debug)
            lock.release()

    def writeFile(self, fileName, contents):

        # check for null values
        if fileName is None:
            raise TypeError
        if contents is None:
            raise TypeError

        try:

            # check if dir exists to receive files, if not, create it anyway, then move to it
            if not os.path.exists(PATH):
                os.makedirs(PATH)
            os.chdir(PATH)

            # create file to write 
            writer = open(fileName, 'w+b') # write and binary
            writer.write(contents)
            writer.close() # close, always good practice to close things when done :)
            # show the user a message
            print("File %s received from %s" % (fileName, self.address))
        except FileNotFoundError:
            print("File Not Found Error: File %s not found" % fileName)
            self.fsock.Status(0, debug)
            sys.exit(1)

if __name__ == "__main__":
    while 1:
        sockAddress = listenSocket.accept()
        server = Server(sockAddress)
        server.start()

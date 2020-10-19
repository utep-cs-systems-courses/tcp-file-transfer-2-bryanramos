#! /usr/bin/env python3

# Author: Bryan Ramos
# Course: Theory of Operating Systems (OS)
# Instructors: Eric Freudenthal and David Pruitt
# Assignment: Lab 2 - TCP File Transfer

import os, socket, sys

sys.path.append("../lib") # for params
import params
from framedSock import framedReceive

FILES_PATH = "./Receive"
HOST = "127.0.0.1"

def server():
    switchesVarDefaults = (
        (('1', '--listenPort'), 'listenPort', 50001),
        (('?', '--usage'), 'usage', False),
        (('d', '--debug'), 'debug', False),
    )

    parameterMap = params.parseParams(switchesVarDefaults)
    listenPort, debug = parameterMap['listenPort'], parameterMap['debug']

    if parameterMap['usage']:
        params.usage()

    bindAddr = (HOST, listenPort)

    # creating listening socket
    listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listenSocket.bind(bindAddr)

    listenSocket.listen(10)
    print("Listening on: ", bindAddr)

    # check if directory exists to receive files, if not, create it, then move to it
    if not os.path.exists(FILES_PATH):
        os.makedirs(FILES_PATH)
    os.chdir(FILES_PATH)

    while True:
        connection, address = listenSocket.accept()

        if not connection or not address:
            sys.exit(1)
        
        if not os.fork():
            print("Connected by", address)

            # receive files from client
            try:
                fileName, contents = framedReceive(connection, debug)
            except:
                print("Errot: File transfer was not successful!")
                connection.sendall(str(0).encode())
                sys.exit(1)

            # try saving the files in receive folder
            fileName = fileName.decode()
            writeFile(connection, address, fileName, contents)

            # send message of success
            connection.sendall(str(1).encode())
            sys.exit(0)

def writeFile(connection, address, fileName, contents):
    if connection is None: 
        raise TypeError
    if address is None: 
        raise TypeError
    if fileName is None:
        raise TypeError
    if contents is None:
        raise TypeError

    try:
        # create file to write 
        writer = open(fileName, 'w+b') # write and binary
        writer.write(contents)
        writer.close() # close, always good practice to close things when done :)

        print("File %s received from %s" % (fileName, address))
    except FileNotFoundError:
        print("File Not Found Error: File %s not found" % fileName)
        connection.sendall(str(0).encode())
        sys.exit(1)

if __name__ == "__main__":
    server()
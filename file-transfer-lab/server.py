#! /usr/bin/env python3

# Author: Bryan Ramos
# Course: Theory of Operating Systems (OS)
# Instructors: Eric Freudenthal and David Pruitt
# Assignment: Lab 2 - TCP File Transfer

import os, socket, sys

sys.path.append("../lib") # for params
import params
from framedSock import framedReceive

PATH = "./Receive"
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

    bindAddress = (HOST, listenPort)

    # creating listening socket
    listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listenSocket.bind(bindAddress)

    listenSocket.listen(10) # 10 connections
    print("Listening on: ", bindAddress)

    # check if dir exists to receive files, if not, create it anyway, then move to it
    if not os.path.exists(PATH):
        os.makeidrs(PATH)
    os.chdir(PATH)

    while 1:
        connection, address = listenSocket.accept()

        # if no connection or no address, get out of there 
        if not connection or not address:
            sys.exit(1)

        if not os.fork():
            print("Connected by: ", address)

            # receive files from client connection
            try:
                fileName, contents = framedReceive(connection, debug)
            except:
                print("Error: File transfer was not successful!")
                connection.sendAll(str(0).encode())
                sys.exit(1)
            
            # save files to 'receive' dir
            fileName = fileName.decode()
            writeFile(connection, address, fileName, contents)

            # return message of success
            connection.sendall(str(0).encode())
            sys.exit(0)

def writeFile(connection, address, fileName, contents):

    # check for null values
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
        # show the user a message
        print("File %s received from %s" % (fileName, address))
    except FileNotFoundError:
        print("File Not Found Error: File %s not found" % fileName)
        connection.sendall(str(0).encode())
        sys.exit(1)

if __name__ == "__main__":
    server()
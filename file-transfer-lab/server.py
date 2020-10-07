#! /usr/bin/env python3

# Author: Bryan Ramos
# Course: Theory of Operating Systems (OS)
# Instructors: Eric Freudenthal and David Pruitt
# Assignment: Lab 2 - TCP File Transfer

import os, socket, sys

sys.path.append("../lib") # for params
import params

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

    # create a listening socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # associating socket with host and port number
        s.bind((HOST, listenPort))

        # makes s the listening socket
        s.listen()
        print("Listening on: ", (HOST, listenPort))

        connection, address = s.accept() # wait until incoming connection request (and accept it)

        os.chdir(FILES_PATH) # switch to directory to receive files

        # based on demos
        with connection:
            print("Connected by", address)
            while 1:
                # receive file name first
                data = connection.recv(1024)
                decodedData = data.decode()

                # if file name was given
                if decodedData:
                    writeFile(decodedData, connection)
                
                if not data:
                    break;
                
                connection.sendall(data)

def writeFile(fileName, connection):
    # create file to write 
    writer = open(fileName, 'wb') # write and binary

    # write, receive data
    data = connection.recv(1024)
    writer.write(data)

    writer.close() # close, always good practice to close things when done :)
    print("File %s received :)" % fileName) 

if __name__ == "__main__":
    server()
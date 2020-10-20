#! /usr/bin/env python3

# Author: Bryan Ramos
# Course: Theory of Operating Systems (OS)
# Instructors: Eric Freudenthal and David Pruitt
# Assignment: Lab 2 - TCP File Transfer w/ Threads

import os, re, socket, sys

sys.path.append("../lib") # for params
import params
from encapFramedSock import EncapFramedSock

PATH = "Send/"

def client():
    switchesVarDefaults = (
        (('1', '--server'), 'server', "127.0.0.1:50001"),
        (('?', '--usage'), 'usage', False),
        (('d', '--debug'), 'debug', False),
    )

    # based on demos
    parameterMap = params.parseParams(switchesVarDefaults);
    server, usage, debug = parameterMap['server'], parameterMap['usage'], parameterMap['debug']

    if usage:
        params.usage();

    try:
        serverHost, serverPort = re.split(":", server)
        serverPort = int(serverPort)
    except:
        print("Can't parse server:port from '%s'" % server)
        sys.exit(1)

    port = (serverHost, serverPort)

     # create socket
    listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listenSocket.connect(port)

    encapSocket = EncapFramedSock((listenSocket, port))

    while 1:
        fileName = input("Enter a filename > ")
        fileName.strip()

        if fileName == "exit": # terminate
            sys.exit(0)
        else:
            if not fileName:
                continue
            elif os.path.exists(PATH + fileName):
                f = open(PATH + fileName, "rb") # read and binary
                contents = f.read()

                if len(contents) < 1:
                    print("Error: File %s is empty" % fileName)
                    continue

                encapSocket.send(fileName, contents, debug)

                # check if server was able to receive the file
                status = encapSocket.Status()
                status = int(status.decode())

                if status:
                    print("File %s received by server." % fileName)
                    sys.exit(0)
                else:
                    print("File Transfer Error: File %s was not received by server." % fileName)
                    sys.exit(1)
                    

            else:
                print("File Not Found Error: File %s not found!" % fileName)

if __name__ == "__main__":
    client()
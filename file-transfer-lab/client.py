#! /usr/bin/env python3

# Author: Bryan Ramos
# Course: Theory of Operating Systems (OS)
# Instructors: Eric Freudenthal and David Pruitt
# Assignment: Lab 2 - TCP File Transfer

import os, re, socket, sys

sys.path.append("../lib") # for params
import params

FILES_PATH = "Send/"

def client():
    switchesVarDefaults = (
        (('1', '--server'), 'server', "127.0.0.1:50001"),
        (('?', '--usage'), 'usage', False),
        (('d', '--debug'), 'debug', False),
    )

    # based on demos

    parameterMap = params.parseParams(switchesVarDefaults);
    server, usage, debug = parameterMap['server'], parameterMap['usage'], parameterMap['debug']

    if parameterMap['usage']:
        params.usage();

    try:
        serverHost, serverPort = re.split(":", server)
        serverPort = int(serverPort)
    except:
        print("Can't parse server:port from '%s'" % server)
        sys.exit(1)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((serverHost, serverPort))

        while 1:
            fileName = input("> ")
            fileName.strip()

            if fileName == "exit": # terminate
                sys.exit(0)
            else:
                if not fileName:
                    continue
                elif os.path.exists(FILES_PATH + fileName):
                    # send filename
                    s.sendall(fileName.encode())
                    contents = open(FILES_PATH + fileName, "rb") # read and binary

                    # send contents
                    while 1:
                        data = contents.read(1024)
                        s.sendall(data)

                        if not data:
                            break

                    contents.close() # always good practice to close things when done :)
                else:
                    print("File %s not found" % fileName)

if __name__ == "__main__":
    client()
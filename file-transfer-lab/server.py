#! /usr/bin/env python3

import os, socket, sys

sys.path.append("../lib") # for params
import params

FILES_PATH = "/Receive"
HOST = "127.0.0.1"

def server():
    switchesVarDefaults = (
        (('1', '--listenPort'), 'listenPort', 50001),
        (('?', '--usage'), 'usage', False),
        (('d', '--debug'), 'debug', False),
    )

    parameterMap = params.parseParams(switchesVarDefaults);
    listenPort, debug = parameterMap['listenPort'], parameterMap['debug']

    if parameterMap['usage']:
        params.usage();

    bindAddr = (HOST, listenPort)

    # create a listening socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # associating socket with host and port number
        s.bind(bindAddr)

        # makes s the listening socket
        s.listen()
        print("Listening on: ", bindAddr)

        connection, address = s.accept() # wait until incoming connection request (and accept it)

        os.chdir(FILES_PATH) # switch to directory to receive files

        with connection:
            print("Connected by", addr)
            while 1:
                # receive file name first
                data = connection.recv(1024).decode()

                # if file name was given
                if data:
                    write_file(data, connection)
                
                if not data:
                    break;
                
                connection.sendAll(data)

if __name__ == "__main__":
    server()
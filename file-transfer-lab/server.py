#! /usr/bin/env python3

import os, socket, sys

sys.path.append("../lib") # for params
import params

FILES_PATH = "/Receive"

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

if __name__ == "__main__":
    server()
#! /usr/bin/env python3

import os, re, socket, sys

sys.path.append("../lib") # for params
import params

FILES_PATH = "/Send"

def client():
    switchesVarDefaults = (
        (('1', '--server'), 'server', "127.0.0.1:50001"),
        (('?', '--usage'), 'usage', False),
        (('d', '--debug'), 'debug', False),
    )

    parameterMap = params.parseParams(switchesVarDefaults);
    server, usage, debug = parameterMap['server'], parameterMap['usage'], parameterMap['debug']

    if parameterMap['usage']:
        params.usage();

if __name__ == "__main__":
    client()
# File Transfer Lab w/ Threads

Author: Bryan Ramos

## Description

* Does not allow empty files to be sent to the server by clients.
* File overwrite for already existing files, per the requirements, we were allowed to handle that how we wanted to.
* Sever can run w/o a proxy.
* This version implements locks when several clients try to send files simulatenously.
* Implemented with Threads using guidance from demo code and lecture notes.

This can run on WSL and Linux.

1. Open a terminal window and navigate to the `file-transfer-lab` directory and run `./server.py`
2. Open another terminal window and navigate to the `file-transfer-lab` directory and run `./client.py` or `./client.py --server 127.0.0.1:50001`.
3. Enter a filename, with its extension, on the prompt from the program. `sprite.png`
4. To exit, type in `exit`.
 
** Note **: To run with a proxy, before Step 1, perform the following step.

Run the proxy by navigating to the `stammer-proxy` directory and running `./stammerProxy.py` on the terminal window. 
import threading 
from weioUserApi import *

from weioMain import *

import socket
import sys
import os


def udsServer():
    server_address = './uds_socket'

    print server_address

    # Make sure the socket does not already exist
    try:
        os.unlink(server_address)
    except OSError:
        if os.path.exists(server_address):
            raise

    # Create a UDS socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    # Bind the socket to the port
    print  'starting up on %s' % server_address
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    while True:
        # Wait for a connection
        print 'waiting for a connection'
        connection, client_address = sock.accept()
        print  'connection from', client_address

        # Receive the data in small chunks and retransmit it
        while True:
            req = connection.recv(128)
            print 'received "%s"' % req
            break
            

def main():
    WeioUserSetup()

    # Start the UDS Server
    threading.Thread(target=udsServer).start()

    for key in attach.procs :
        print key
        t = threading.Thread(target=attach.procs[key].procFnc, args=attach.procs[key].procArgs)
        #t.daemon = True
        t.start()

if __name__ == "__main__":
    main()

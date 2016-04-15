import zmq
import random
import sys
import time

from crypt import AESCipher

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind("tcp://*:%s" % port)

def poll_socket(socket, timetick = 100):
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)
    # wait up to 100msec
    try:
        while True:
            obj = dict(poller.poll(timetick))
            if socket in obj and obj[socket] == zmq.POLLIN:
                yield socket.recv()
    except KeyboardInterrupt:
        pass

for message in poll_socket(socket):
    handle_message(message)

#time.sleep(10)
socket.close()

while True:
    socket.send("Server message to client3")
    msg = socket.recv()
    print msg
    time.sleep(1)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL);

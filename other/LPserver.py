from random import randint
import time
import zmq
import signal
from logger import log, get_user_type
from RSA import send, recv
import rsa


# DEFINITIONS
user_type = get_user_type() # Receives user input log settings
context = zmq.Context(1)

server = context.socket(zmq.REP)
server.bind("tcp://*:5555")

# Enter messages for encryption
#print "### Hello! Type your secret message below ###"
#message = raw_input('>: ')

(pub_key, priv_key) = rsa.newkeys(512)

#print "IN: ", msg_en
#print "OUT: ", msg_de

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

cycles = 0
while True:
    request = server.recv()
    if RepresentsInt(request) == False:
        message = recv(request, priv_key)
        print "OUT: ", message
    cycles += 1

    # Simulate various problems, after a few cycles
    if cycles > 3 and randint(0, 3) == 0:
        log(user_type, 'INFO', 'Simulating a crash')
        break
    elif cycles > 3 and randint(0, 3) == 0:
        log(user_type, 'INFO', 'Simulating CPU overload')
        time.sleep(2)
    log(user_type, 'INFO', 'Normal request (%s)' % request)
    time.sleep(1) # Do some heavy work
    server.send(request)

server.close()
context.term()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL);

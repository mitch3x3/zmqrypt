import sys
import zmq
import signal
import rsa
from logger import log, get_user_type
from RSA import send, recv, b64_encode, b64_decode

print "IP: "
ip_address = raw_input('>: ')
#print "PUBLIC KEY: "
#pub_key = raw_input('>: ')
(pub_key, priv_key) = rsa.newkeys(512)

# DEFINITIONS
user_type = get_user_type() # Receives user input log settings
REQUEST_TIMEOUT = 2500
REQUEST_RETRIES = 3
SERVER_ENDPOINT = "tcp://%s:5555" % ip_address
context = zmq.Context(1)

# MAIN CODE
log(user_type, 'INFO', 'Connecting to server')
client = context.socket(zmq.REQ)
client.connect(SERVER_ENDPOINT)

poll = zmq.Poller()
poll.register(client, zmq.POLLIN)

# Enter messages for encryption
print "### Hello! Type your secret message below ###"
message = raw_input('>: ')
crypt_msg = send(message, pub_key)
#message = recv(crypt_msg, priv_key)
print "IN: ", crypt_msg
#print "OUT: ", msg_de


sequence = 0
retries_left = REQUEST_RETRIES
while retries_left:
    sequence = crypt_msg
    request = str(sequence)
    client.send(request)
    log(user_type, 'INFO', 'Sending (%s)' % request)

    expect_reply = True
    while expect_reply:
        socks = dict(poll.poll(REQUEST_TIMEOUT))
        if socks.get(client) == zmq.POLLIN:
            reply = client.recv()
            if not reply:
                break
            if int(reply) == sequence:
                log(user_type, 'INFO', 'Server replied OK (%s)' % reply)
                retries_left = REQUEST_RETRIES
                expect_reply = False
            else:
                log(user_type, 'ERROR', 'Malformed reply from server: %s' % reply)

        else:
            log(user_type, 'WARNING', 'No response from server, retrying')
            # Socket is confused. Close and remove it.
            client.setsockopt(zmq.LINGER, 0)
            client.close()
            poll.unregister(client)
            retries_left -= 1
            if retries_left == 0:
                log(user_type, 'ERROR', 'Server seems to be offline, abandoning')
                break
            log(user_type, 'INFO', 'Reconnecting and resending (%s)' % request)
            # Create new connection
            client = context.socket(zmq.REQ)
            client.connect(SERVER_ENDPOINT)
            poll.register(client, zmq.POLLIN)
            client.send(request)

context.term()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL);

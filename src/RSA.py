#!/usr/bin/python
# -*- coding: utf-8 -*-
#

import rsa
import time
import base64


def send(message, pubkey):
    crypt_msg = rsa.encrypt(message, pubkey)
    return crypt_msg
    
def recv(crypt, privkey):
    message = rsa.decrypt(crypt, privkey)
    return message

def b64_encode(public_key):
    key = str(public_key.n) + str(public_key.e)
    b64_key = base64.b64encode(key)
    return b64_key

def b64_decode(b64_key):
    b64de = base64.b64decode(b64_key)
    n = int(b64de[:-5])
    e = int(b64de[-5:])
    public_key = rsa.PublicKey(n, e)
    return public_key

'''
msg_A = ''
while (msg_A != 'exit'):
    msg_A = raw_input('>: ')

    if len(msg_A) <= 53:
        crypt_msg = send(msg_A, pubkey_B)
        message = recv(crypt_msg, privkey_B)
        if msg_A != 'exit':
            print 'A: '+message
    else:
        print '### MESSAGE DID NOT SEND ###'
        print 'Error: Message contained more than 53 characters'

print 'Connection terminated'
'''

#(pubkey_A, privkey_A) = rsa.newkeys(512)
#(pubkey_B, privkey_B) = rsa.newkeys(512)


#b64_key = b64_encode(pubkey_B)

#print 'Peers Public Key: ' + str(b64_key)

#print 'Enter Peers Public Key: '
#key = raw_input('>: ')

#pub_key = b64_decode(key)
#msg_A = raw_input('>: ')
#crypt_msg = send(msg_A, pub_key)
#message = recv(crypt_msg, privkey_B)
#print 'A: '+message


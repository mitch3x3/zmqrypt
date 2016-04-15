'''
from Crypto.Cipher import AES
from Crypto import Random
import base64
import os

def encryption(privateInfo):
    block_size = 16
    padding = ' { '

    pad = lambda s: s + (block_size - len(s) % block_size) * padding

    EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))

    secret = os.urandom(block_size)
    print 'encryption key: ', secret

    cipher = AES.new(secret)

    encoded = EncodeAES(cipher, privateInfo)

    print "Encrypted String: ", encoded

#encryption('CCCCEEEEWWWWRRRR')
'''

import base64
from Crypto.Cipher import AES
import os
import random
import string

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[:-ord(s[len(s)-1:])]

def generate_hex_pin():
    hex_pin = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for i in range(BS))
    return hex_pin
    
class AESCipher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, raw):
        raw = pad(raw)
        iv = os.urandom(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:]))

#!/usr/bin/python
# -*- coding: utf-8 -*-
#

import sys, time
import signal
import zmq
#from keypress import read_single_keypress
#read_single_keypress()
from kbhit import KBHit

kb = KBHit()

mode_toggle = True

pub_port = "5555"
sub_port = "5556"
topic = "10001"
topicfilter = "10001"
context = zmq.Context()

pub_socket = context.socket(zmq.PUB)
pub_socket.bind("tcp://*:%s" % pub_port)
sub_socket = context.socket(zmq.SUB)
sub_socket.connect("tcp://localhost:%s" % sub_port)
sub_socket.setsockopt(zmq.SUBSCRIBE, topicfilter)

while True:
    while not mode_toggle:
        print "Receiving:"
        if kb.getch() == 'r':
            msg = sub_socket.recv()
            print 'B: ' + msg
            time.sleep(1)
            mode_toggle = not mode_toggle
            break
        if kb.getch() == 'q':
            mode_toggle = not mode_toggle
            break

    while mode_toggle:
        print "Sending:"
        if kb.getch() == 'z':
            message = raw_input('>: ')
            pub_socket.send("%s %s" % (topic, message))
            mode_toggle = not mode_toggle
            break
        if kb.getch() == 'q': # ESC
            mode_toggle = not mode_toggle
            break
        

def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)		# KeyboardInterrupt -> ^C
    

if __name__ == '__main__':
    main()
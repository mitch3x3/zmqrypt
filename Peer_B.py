#!/usr/bin/python
# -*- coding: utf-8 -*-
#
import sys, time
import signal
import zmq

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
    string = sub_socket.recv()
    msg = string[5:]
    topic = string[:5]
    print 'A: ' + msg
    
def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)		# KeyboardInterrupt -> ^C
    

if __name__ == '__main__':
    main()
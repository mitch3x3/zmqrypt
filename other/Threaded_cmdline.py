#!/usr/bin/python
# -*- coding: utf-8 -*-
#

from PyQt4 import QtCore
import time
import sys
import zmq

pub_port = "5555"
sub_port = "5555"
topic = "10001"
topicfilter = "10001"
context = zmq.Context()

pub_socket = context.socket(zmq.PUB)
pub_socket.bind("tcp://*:%s" % pub_port)
sub_socket = context.socket(zmq.SUB)
sub_socket.connect("tcp://localhost:%s" % sub_port)
sub_socket.setsockopt(zmq.SUBSCRIBE, topicfilter)


class AThread(QtCore.QThread):
        
    def run(self):
        while True:
            string = sub_socket.recv()
            message = string[5:]
            #topic = string[:5]
            #self.add_B(message)
            print "Thread A: " + str(message)

class BThread(QtCore.QThread):

    def run(self):
        while True:
            time.sleep(1)
            message = raw_input('>: ')
            pub_socket.send("%s %s" % (topic, message))
            
def main():
    app = QtCore.QCoreApplication([])
    thread_A = AThread()
    thread_A.finished.connect(app.exit)
    thread_A.start()
    thread_B = BThread()
    thread_B.finished.connect(app.exit)
    thread_B.start()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
    
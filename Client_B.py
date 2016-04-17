import sys, time, os
import signal
from PyQt4 import QtCore, QtGui
import zmq
import random

class MainWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
     
        self.setGeometry(300, 300, 320, 300)
        self.setWindowTitle('ZMQrypt Messenger B')
     
        self.layout = QtGui.QGridLayout(self)
         
        self.message_entry = QtGui.QLineEdit(self)
        self.sendButton = QtGui.QPushButton("Send")
        self.recvButton = QtGui.QPushButton("Recv")
        self.connect(self.sendButton, QtCore.SIGNAL("released()"), self.send)
        self.connect(self.recvButton, QtCore.SIGNAL("released()"), self.receive)
        self.listwidget = QtGui.QListWidget(self)
        self.ip_entry = QtGui.QLineEdit(self)
        self.ip_address = QtGui.QLabel(self)
     	self.ip_address.setText("IP Address: ")
        self.ip_set = QtGui.QPushButton("Set")
        #self.connect(self.startButton, QtCore.SIGNAL("released()"), self.test)
    
        self.layout.addWidget(self.ip_address, 0, 0, 1, 1)
        self.layout.addWidget(self.ip_entry, 0, 1, 1, 2)
        self.layout.addWidget(self.ip_set, 0, 3, 1, 1)
        self.layout.addWidget(self.listwidget, 1, 0, 1, 4)
        self.layout.addWidget(self.message_entry, 2, 0, 1, 2)
        self.layout.addWidget(self.sendButton, 2, 2, 1, 1)
        self.layout.addWidget(self.recvButton, 2, 3, 1, 1)
        
        pub_port = "5555"
        sub_port = "5556"
        self.topic = "10001"
        self.topicfilter = "10001"
        context = zmq.Context()

        self.pub_socket = context.socket(zmq.PUB)
        self.pub_socket.bind("tcp://*:%s" % pub_port)

        self.sub_socket = context.socket(zmq.SUB)
        self.sub_socket.connect("tcp://localhost:%s" % sub_port)
        self.sub_socket.setsockopt(zmq.SUBSCRIBE, self.topicfilter)
        
        #self.timer = QtCore.QTimer(self)
        #self.timer.timeout.connect(self.receive)
        #self.timer.start(1000)

        
    def send(self):
        user_input = self.message_entry.text()
        message = str(user_input)
        #user_input = user_input.encode('ascii')
        self.pub_socket.send_string("%s%s" % (self.topic, message))
        self.add_A(message)
        self.message_entry.clear()
    
    def receive(self):
        string = self.sub_socket.recv()
        message = string[5:]
        topic = string[:5]
        self.add_B(message)
    
    def add_A(self, text):
        self.listwidget.addItem("A: " + text)
        
    def add_B(self, text):
        self.listwidget.addItem("B: " + text)

'''        
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
'''

def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)		# KeyboardInterrupt -> ^C
    app = QtGui.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()

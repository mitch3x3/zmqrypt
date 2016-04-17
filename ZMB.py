import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
import time, os
import signal
import zmq
import random
import rsa
from RSA import send, recv, b64_encode, b64_decode

class MainWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(600, 300, 320, 300)
        self.setWindowTitle('ZMQrypt Messenger B')   
        self.layout = QtGui.QGridLayout(self)
        
        self.peer_ip = None
        self.peer_pub_key = None
        self.encryption_bool = False
        
        self.message_entry = QtGui.QLineEdit(self)
        self.sendButton = QtGui.QPushButton('Send', self)
        self.listwidget = QtGui.QListWidget(self)
        self.ip_entry = QtGui.QLineEdit(self)
        self.ip_address = QtGui.QLabel(self)
        self.ip_address.setText("IP Address: ")
        self.ip_set = QtGui.QPushButton("Set")
        self.peer_pub_entry = QtGui.QLineEdit(self)
        self.peer_key = QtGui.QLabel(self)
        self.peer_key.setText("Peer's Public Key: ")
        self.key_set = QtGui.QPushButton("Set")
        
        self.sendButton.clicked.connect(self.send)
        self.ip_set.clicked.connect(self.connect)
        #self.ip_set.clicked.connect(self.give_handshake)
        self.key_set.clicked.connect(self.recv_handshake)
        
        #self.label = QtGui.QLabel('Count = 0', self)
        #self.button = QtGui.QPushButton('Start', self)
        #self.button.clicked.connect(self.handleButton)
        #layout = QtGui.QVBoxLayout(self)
        self.layout.addWidget(self.ip_address, 0, 0, 1, 1)
        self.layout.addWidget(self.ip_entry, 0, 1, 1, 2)
        self.layout.addWidget(self.ip_set, 0, 3, 1, 1)
        self.layout.addWidget(self.peer_key, 1, 0, 1, 1)
        self.layout.addWidget(self.peer_pub_entry, 1, 1, 1, 2)
        self.layout.addWidget(self.key_set, 1, 3, 1, 1)
        self.layout.addWidget(self.listwidget, 2, 0, 1, 4)
        self.layout.addWidget(self.message_entry, 3, 0, 1, 3)
        self.layout.addWidget(self.sendButton, 3, 3, 1, 1)

        #layout.addWidget(self.button)
        self._active = False
        

    def send(self):
        if self.encryption_bool == False:
            self.reg_send()
        else:
            self.en_send()
    
    def reg_send(self):
        if not self._active:
            user_input = self.message_entry.text()
            message = str(user_input)
            pub_socket.send(message)
            self.add_A(message)
            self.message_entry.clear()
            #QtCore.QTimer.singleShot(0, self.runLoop)
        else:
            self._active = False
    
    def en_send(self):
        if not self._active:
            user_input = self.message_entry.text()
            message = str(user_input)
            crypt_msg = send(message, self.peer_pub_key)
            #user_input = user_input.encode('ascii')
            pub_socket.send("%s%s" % (topic, crypt_msg))
            print "IN: ", crypt_msg
            self.add_A(message)
            self.message_entry.clear()
            #QtCore.QTimer.singleShot(0, self.runLoop)
        else:
            self._active = False
    
    def give_handshake(self):
        b64_key = b64_encode(pub_key)
        pub_socket.send_string("%s" % str(b64_key))
        string = sub_socket.recv()
        request = string[5:]
        w.add_B(request)
    
    def recv_handshake(self):
        self.encryption_bool = True
        user_input = self.peer_pub_entry.text()
        self.peer_pub_key = str(user_input)
    
    def connect(self):
        user_input = self.ip_entry.text()
        self.peer_ip = str(user_input)
    
    def add_A(self, text):
        self.listwidget.addItem("A: " + text)
        
    def add_B(self, text):
        self.listwidget.addItem("B: " + text)

# very testable class (hint: you can use mock.Mock for the signals)
class Worker(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    #dataReady = QtCore.pyqtSignal(list, dict)

    @QtCore.pyqtSlot()
    def processA(self):
        connection = False
        c_bool = True
        while c_bool:
            if w.peer_ip != None:
                try:
                    sub_socket.connect("tcp://{0}:{1}".format(w.peer_ip, sub_port))
                    #sub_socket.setsockopt(zmq.SUBSCRIBE, topicfilter)
                    connection = True
                    print "Connected to: " + str(w.peer_ip) + ":" + str(sub_port)
                    c_bool = False
                    
                except:
                    connection = False
                    print "Invalid IP Address"
        
        if connection == True and w.encryption_bool == False: 
            print "Regular messaging"
            while True:
                message = sub_socket.recv()
                w.add_B(message)
                print "B: " + str(message)
            self.finished.emit()
        
        if connection == True and w.encryption_bool == True: 
            while True:
                string = sub_socket.recv()
                request = string[5:]
                #topic = string[:5]
                message = recv(request, priv_key)
                w.add_B(message)
                #print "B: " + str(message)
            self.finished.emit()
                
    @QtCore.pyqtSlot()
    def processB(self):
        b64_key = b64_encode(pub_key)
        
        c_bool = True
        #hs_bool = True
        while c_bool:
            if w.peer_ip != None:
                try:
                    sub_socket.connect("tcp://{0}:{1}".format(w.peer_ip, sub_port))
                    sub_socket.setsockopt(zmq.SUBSCRIBE, topicfilter)
                    connection = True
                    print "Connected to: " + str(w.peer_ip) + ":" + str(sub_port)
                    c_bool = False
                    
                except:
                    connection = False
                    print "Invalid IP Address"
        
        #while hs_bool:
            #client_receiver.RCVTIMEO = 1000
            #poller = zmq.Poller()
            #poller.register(client_receiver, zmq.POLLIN)
            #evts = poller.poll(1000)
            #print evts
            #pub_socket.send_string("%s" % str(b64_key), zmq.NOBLOCK)
            #string = sub_socket.recv(flags=zmq.NOBLOCK)
            #request = string[5:]
            #print request
            #hs_bool = False
            
        self.finished.emit()

if __name__ == '__main__':
    
    app = QtGui.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    thread = QtCore.QThread()  # no parent!
    obj = Worker()  # no parent!
    #obj.dataReady.connect(onDataReady)
    
    pub_port = "5555"
    sub_port = "5556"
    topic = "10001"
    topicfilter = "10001"
    context = zmq.Context()
    
    sub_socket = context.socket(zmq.SUB)
    #sub_socket.setsockopt(zmq.SUBSCRIBE, topicfilter)
    pub_socket = context.socket(zmq.PUB)
    pub_socket.bind("tcp://*:%s" % pub_port)
    
    (pub_key, priv_key) = rsa.newkeys(512)
    
    obj.moveToThread(thread)
    obj.finished.connect(thread.quit)
    thread.started.connect(obj.processB)
    thread.finished.connect(app.exit)
    thread.start()
    thread.started.connect(obj.processA)
    thread.finished.connect(app.exit)
    thread.start()

    sys.exit(app.exec_())
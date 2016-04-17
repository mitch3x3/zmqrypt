import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
import time, os
import signal
import zmq
import random

class MainWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(600, 300, 320, 300)
        self.setWindowTitle('Simple ZMQ Messenger')   
        self.layout = QtGui.QGridLayout(self)
        
        self.peer_ip = None
        
        self.message_entry = QtGui.QLineEdit(self)
        self.sendButton = QtGui.QPushButton('Send', self)
        self.listwidget = QtGui.QListWidget(self)
        self.ip_entry = QtGui.QLineEdit(self)
        self.ip_address = QtGui.QLabel(self)
        self.ip_address.setText("IP Address: ")
        self.ip_set = QtGui.QPushButton("Set")
        
        self.sendButton.clicked.connect(self.send)
        self.ip_set.clicked.connect(self.connect)
        
        #self.label = QtGui.QLabel('Count = 0', self)
        #self.button = QtGui.QPushButton('Start', self)
        #self.button.clicked.connect(self.handleButton)
        #layout = QtGui.QVBoxLayout(self)
        self.layout.addWidget(self.ip_address, 0, 0, 1, 1)
        self.layout.addWidget(self.ip_entry, 0, 1, 1, 2)
        self.layout.addWidget(self.ip_set, 0, 3, 1, 1)
        self.layout.addWidget(self.listwidget, 1, 0, 1, 4)
        self.layout.addWidget(self.message_entry, 2, 0, 1, 3)
        self.layout.addWidget(self.sendButton, 2, 3, 1, 1)

        #layout.addWidget(self.button)
        self._active = False
        

    def send(self):
        if not self._active:
            user_input = self.message_entry.text()
            message = str(user_input)
            #user_input = user_input.encode('ascii')
            pub_socket.send_string("%s%s" % (topic, message))
            self.add_A(message)
            self.message_entry.clear()
            #QtCore.QTimer.singleShot(0, self.runLoop)
        else:
            self._active = False
    
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
                    sub_socket.setsockopt(zmq.SUBSCRIBE, topicfilter)
                    connection = True
                    print "Connected to: " + str(w.peer_ip) + ":" + str(sub_port)
                    c_bool = False
                except:
                    connection = False
                    print "Invalid IP Address"
            
        if connection == True:        
            while True:
                string = sub_socket.recv()
                message = string[5:]
                #topic = string[:5]
                w.add_B(message)
                #print "B: " + str(message)
            self.finished.emit()
                
    @QtCore.pyqtSlot()
    def processB(self):
        print "Worker.processB()"
        while True:
            time.sleep(1)
            message = raw_input('>: ')
            pub_socket.send("%s %s" % (topic, message))
        self.finished.emit()

if __name__ == '__main__':
    
    app = QtGui.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    thread = QtCore.QThread()  # no parent!
    obj = Worker()  # no parent!
    #obj.dataReady.connect(onDataReady)
    
    pub_port = "5555"
    sub_port = "5555"
    topic = "10001"
    topicfilter = "10001"
    context = zmq.Context()

    pub_socket = context.socket(zmq.PUB)
    pub_socket.bind("tcp://*:%s" % pub_port)
    sub_socket = context.socket(zmq.SUB)
    
    
    obj.moveToThread(thread)
    obj.finished.connect(thread.quit)
    thread.started.connect(obj.processA)
    thread.finished.connect(app.exit)
    thread.start()

    sys.exit(app.exec_())
import time
import struct
import threading
import socket
from math import sin

class Data():
    def __init__(self):
        self.connected = False
        self.fmt = '>Q'
        for _ in range(132):
            self.fmt += 'd'
        self.s = None
        self.package_size = 0
        self.time = 0
        self.qtarget = [0, 0, 0, 0, 0, 0]
        self.qdtarget = [0, 0, 0, 0, 0, 0]
        self.qddtarget = [0, 0, 0, 0, 0, 0]
        self.qactual = [0, 0, 0, 0, 0, 0]
        self.tool_frame = [0, 0, 0, 0, 0, 0]
        self.program_state = 0
        self.thread = threading.Thread(target=self.read)

    def connect(self, ip, simulate=False):
        TCP_IP = ip
        TCP_PORT = 30003
        BUFFER_SIZE = 1060

        self.simulate = simulate

        if not self.simulate:
            if not self.connected:
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.settimeout(10)
                try:
                    print("Opening IP Address " + TCP_IP)
                    self.s.connect((TCP_IP, TCP_PORT))
                    self.s.recv(BUFFER_SIZE)
                    self.connected = True
                except socket.error:
                    print("Socket error")
                    self.s.close()
        else:
            self.connected = True

        if self.connected:
            self.thread.start()

    def disconnect(self):
        if self.connected:
            print('Stopping thread')
            self.connected = False
            if self.s is not None:
                self.s.close()
            time.sleep(1)
            print('Thread stopped')

    def read(self):
        if not self.simulate:
            while self.connected:
                BUFFER_SIZE = 1060
                response = self.s.recv(BUFFER_SIZE)
                self.parse_message(response)
        else:
            while self.connected:
                self.time += 1
                time.sleep(0.05)
                self.qactual[0] = 360*sin(self.time*0.05)
        print('Thread finished')

    def parse_message(self, data):
        data = b'\x00\x00\x00\x00' + data

        if len(data) == 1064:
            print(time.time())
            t = struct.unpack(self.fmt, data)

            self.package_size = t[0]
            self.time = t[1]
            self.qtarget = t[2:6]
            self.qdtarget = t[8:8]
            self.qddtarget = t[16:8]
            self.qactual = t[32:6]
            self.tool_frame = t[56:6]
            self.program_state = t[-1]

class Programmer():
    def __init__(self):
        #Socket til at sende kommandoer til robotten
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(10)
        self.connected = False

    def connect(self, ip='10.130.58.13'):
        TCP_IP = ip
        TCP_PORT = 30002
        BUFFER_SIZE = 1024

        try:
            print("Opening IP Address " + TCP_IP)
            self.s.connect((TCP_IP, TCP_PORT))
            self.s.recv(BUFFER_SIZE)
            self.connected = True
        except socket.error:
            print("Socket error")
            self.s.close()

    def move_home(self):
        if self.connected:
            #Prædefineret home-position:
            #(Når vi skal sende en streng til robotten,
            # skal den konverteres til et bytearrayself.
            # derfor står der b' foran strengen.)
            self.s.send(b'  movel(p[0, -0.4, 0.15, 0, 3.14, 0])\n')

    def move_xyz(self, x, y, z):
        if self.connected:
            #Når vi skal sende en streng til robotten,
            # skal den konverteres til et bytearrayself.
            # derfor står der b' foran strengen.
            self.s.send(b'def myProg():\n')
            #Vi læser robottens aktuelle konfiguration,
            # for at genbruge rotationen.
            self.s.send(b'  var_1=get_actual_tcp_pose()\n')
            st = '  var_1[0] = {}\n'.format(x)
            # Hvis vi har indsat en værdi i strengen
            # med format, skal strengen konverteres
            # til et bytearray, før den sendes til robotten.
            self.s.send(bytearray(st, 'utf8'))
            st = '  var_1[1] = {}\n'.format(y)
            self.s.send(bytearray(st, 'utf8'))
            st = '  var_1[2] = {}\n'.format(z)
            self.s.send(bytearray(st, 'utf8'))
            self.s.send(b'  movel(var_1)\n')
            self.s.send(bytearray(st, 'utf8'))
            self.s.send(b'end\n')

    def move_curve(self, xy, offset, draw_height):
        offset_x, offset_y = offset
        
        if self.connected:
            self.s.send(b'def myProg():\n')
            self.s.send(b'  var_1=get_actual_tcp_pose()\n')

            st = '  var_1[0] = {}\n'.format(xy[0][0] + offset_x)
            self.s.send(bytearray(st, 'utf8'))
            st = '  var_1[1] = {}\n'.format(xy[0][1] + offset_y)
            self.s.send(bytearray(st, 'utf8'))
            self.s.send(b'  movel(var_1, r=0.01)\n')
            st = '  var_1[2] = {}\n'.format(draw_height)
            self.s.send(bytearray(st, 'utf8'))
            self.s.send(b'  movel(var_1, r=0.01)\n')

            for coords in xy:
                x, y = coords
                x = float(x)/1000
                y = float(y)/1000
                st = '  var_1[0] = {}\n'.format(x + offset_x)
                self.s.send(bytearray(st, 'utf8'))
                st = '  var_1[1] = {}\n'.format(y + offset_y)
                self.s.send(bytearray(st, 'utf8'))
                self.s.send(b'  movel(var_1, r=0.01)\n')
            
            self.move_home()
            self.s.send(b'end\n')

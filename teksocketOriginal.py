import socket
import numpy as np


class TekSocket:
    def __init__(self, ipAddr, port=4000):
        self.ipAddr = ipAddr
        self.port = port
        self.reconnect()

    def reconnect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ipAddr, self.port))
        self.sock.settimeout(0.125) #0.125 - 7 secs lets stick with this

    def getData(self, channels, start=1, stop=0):
        '''
        channels - a list of unique ints, e.g. [1,2,4]
        start - starting index, default is first sample
        stop - ending sample index, default is last sample
        '''
        #self.command(':data:source %s' % channels[0])
        #num_channels = self.command('WFMOutpre:WFMTYPe?')
        #print(num_channels)
        wfidStr = self.command("wfmoutpre:wfid?")
        numPoints = int(wfidStr.split(',')[4].split()[0])

        if start < 1:         start = 1
        if start > numPoints: start = numPoints
        if stop < 1:          stop = numPoints
        if stop > numPoints:  stop = numPoints

        numDataPoints = stop - start + 1

        arrays = []
        for channel in channels:
            # self.command(':data:source ch%d'%channel)
            self.command(':data:source %s' % channel)
            self.command(':data:start %d' % start)
            self.command(':data:stop %d' % stop)
            self.command(':data:encdg ascii')
            self.command(':header 0')
            deltaX = float(self.command('wfmoutpre:xincr?'))
            xZero = float(self.command('wfmoutpre:xzero?'))
            yMult = float(self.command('wfmoutpre:ymult?'))
            yOffset = float(self.command('wfmoutpre:yoff?'))
            yZero = float(self.command('wfmoutpre:yzero?'))
            yOffset *= yMult

            dataStr = self.command(':curve?')

            # echo back to user
            # span = self.command('RF:SPAN?')
            # print('span: {}'.format(span))
            # print('wfmoutpre:xincr? {}'.format(deltaX))
            # print('wfmoutpre:xzero? {}'.format(xZero))
            # print('wfmoutpre:ymult? {}'.format(yMult))
            # print('wfmoutpre:yoff? {}'.format(yOffset))
            # print('wfmoutpre:yzero? {}'.format(yZero))

            data_list = list(map(float, dataStr.split(',')))
            data = np.array(data_list)
            data *= yMult
            data -= yOffset
            arrays.append(data)

        time = np.linspace(xZero,
                           xZero + deltaX * (numDataPoints - 1),
                           numDataPoints)

        arrays.insert(0, time)
        return np.array(arrays).T

    def write(self, msg):
        if len(msg) == 0: return
        if msg[-1] != '\n': msg += '\n'
        sent = self.sock.send(bytes(msg, 'utf-8'))
        while sent != len(msg):
            sent += self.sock.send(msg[sent:])
        return

    def read(self):
        msg = None
        try:
            msg = self.sock.recv(1024)
            while msg[-1] != '\r':
                msg += self.sock.recv(1024)
            return msg.strip()
        except socket.timeout as e:
            err = e.args[0]
            if msg != None:
                return msg.strip()
            print(err)
        return None

    def command(self, msg):
        self.write(msg)
        if '?' in msg:
            x = self.read()
            if x is None:
                return None
            return x.decode("utf-8")
        else:
            return None

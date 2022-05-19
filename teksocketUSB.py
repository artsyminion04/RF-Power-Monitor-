import time
import numpy as np
import pyvisa as visa


class TekSocketUSB:
    def __init__(self, vendor_id, model_id, serial_number):
        self.scope = None
        # rm is the pyvisa object
        self.rm = visa.ResourceManager()
        self.vendor_id = vendor_id
        self.model_id = model_id
        self.serial_number = serial_number
        self.reconnect()


    def reconnect(self):
        resource_tup = self.rm.list_resources()
        # print("resources: {}".format(resource_tup))
        resource_name = None
        for resource in resource_tup:
            if self.vendor_id in resource and self.model_id in resource and self.serial_number in resource:
                resource_name = resource
                break
        # print("resource name: {}".format(resource_name))
        if resource_name is not None:
            # test termination character here
            self.scope = self.rm.open_resource(resource_name)
            #write_termination = '0xA', read_termination = '0xA')
            #self.scope.send_end = True
            #self.scope.read_termination = r'\r\n'
            #self.scope.write_termination = r'\r\n'
            #self.scope.write(r"*IDN?\n")
            #self.scope.read_raw()


    def getData(self, channels, start=1, stop=0):
        '''
        channels - a list of unique ints, e.g. [1,2,4]
        start - starting index, default is first sample
        stop - ending sample index, default is last sample
        '''
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
        self.scope.write(msg)
        return

    def command(self, msg):
        if '?' in msg:
            res = self.scope.query(msg)
            return res
        else:
            self.write(msg)
            return None
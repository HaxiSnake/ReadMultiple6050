import serial
import sys
import time
import numpy as np
import threading 
import signal
import struct
import logging

MAIN_STOP_FLAG = False
class Read6050(threading.Thread):
    def __init__(self,Port='COM0',Baudrate=115200,ByteSize="8", Parity="N", Stopbits="1"):
        threading.Thread.__init__(self)
        self.l_serial = None
        self.alive = False
        self.port = Port
        self.baudrate = Baudrate
        self.bytesize = ByteSize
        self.parity = Parity
        self.stopbits = Stopbits
        self.usRxLength = 0
        self.usLength   = 0
        self.data = np.zeros((3,3),dtype='float16')
    def open(self):
        '''
        打开串口
        '''
        self.l_serial = serial.Serial()
        self.l_serial.port = self.port
        self.l_serial.baudrate = self.baudrate
        self.l_serial.bytesize = int(self.bytesize)
        self.l_serial.parity = self.parity
        self.l_serial.stopbits = int(self.stopbits)
        self.l_serial.timeout = 1
        
        try:
            self.l_serial.open()
            if self.l_serial.isOpen():
                self.alive = True
                #print ("serial start ",self.port)
        except Exception as e:
            self.alive = False
            logging.error(e)
        self.buff = self.l_serial.read(0)
        #print ("read buff ",self.port)
    def stop(self):
        '''
        结束，关闭串口
        '''
        self.alive = False
        if self.l_serial.isOpen():
            self.l_serial.close()
    def run(self):
        '''
        循环读取解析数据
        '''
        count = 0
        while self.alive:
            try:
                temp = self.l_serial.read(1)
                self.buff = self.buff + temp
                self.usLength = len(temp)
                if self.usLength > 0:
                    self.usRxLength = self.usRxLength + self.usLength
                    while self.usRxLength >= 11:
                        packType = str(self.usRxLength)+'b'
                        tempBuff = struct.unpack(packType,self.buff[:self.usRxLength])
                        #tempBuff = [int(hex(x),16) for x in self.buff[:self.usRxLength]]
                        if (((tempBuff[0] == 0x55)  & \
                            ((tempBuff[1] == 0x51) | \
                            (tempBuff[1] == 0x52) | \
                            (tempBuff[1] == 0x53))) is False ):
                            self.buff = self.buff[1:self.usRxLength]
                            self.usRxLength = self.usRxLength - 1
                            continue
                        self.data = self.DecodeData(tempBuff)
                        count = count + 1
                        #print (self.data,count)
                        self.buff = self.buff[11:self.usRxLength]
                        self.usRxLength -= 11
                
            except Exception as e:
                logging.error(e)

    def DecodeData(self,tempBuff,a=np.array([0,0,0],dtype='float16'),\
                    w=np.array([0,0,0],dtype='float16'),\
                    T=np.array([0],dtype='float16'),\
                    angle=np.array([0,0,0],dtype='float16')):
        # a=np.array([0,0,0],dtype='float16')
        # w=np.array([0,0,0],dtype='float16')
        # T=np.array([0],dtype='float16')
        # angle=np.array([0,0,0],dtype='float16')
        if (tempBuff[1]==0x51):
            a[0] =  self.number(tempBuff[2:4])/32768.0*16
            a[1] =  self.number(tempBuff[4:6])/32768.0*16
            a[2] =  self.number(tempBuff[6:8])/32768.0*16
            T[0] =  self.number(tempBuff[8:10])/340.0 + 36.25
            #print ("Xa=%2.3f\tYa=%2.3f\tZa=%2.3f\tT=%3.3f"%(a[0],a[1],a[2],T[0]))
        elif (tempBuff[1]==0x52):
            w[0] =  self.number(tempBuff[2:4])/32768.0*2000
            w[1] =  self.number(tempBuff[4:6])/32768.0*2000
            w[2] =  self.number(tempBuff[6:8])/32768.0*2000
            T[0] =  self.number(tempBuff[8:10])/340.0 + 36.25
            #print ("Xw=%2.3f\tYw=%2.3f\tZw=%2.3f\tT=%3.3f"%(w[0],w[1],w[2],T[0]))
        elif (tempBuff[1]==0x53):
            angle[0] =  self.number(tempBuff[2:4])/32768.0*180
            angle[1] =  self.number(tempBuff[4:6])/32768.0*180
            angle[2] =  self.number(tempBuff[6:8])/32768.0*180
            T[0] =  self.number(tempBuff[8:10])/340.0 + 36.25
            #print ("Xangle=%2.3f\tYangle=%2.3f\tZangle=%2.3f\tT=%3.3f"%(angle[0],angle[1],angle[2],T[0]))
        return np.array([a,w,angle],dtype='float16')
    def number(self,buff):
        HL = np.array([0,0],dtype='b')#HighBit LowBit
        SI = np.array([0],dtype='i2') #ShortInt
        HL[0]=buff[1]
        HL[1]=buff[0]
        SI=HL[0]<<8|HL[1]
        return SI
# def signal_handler(signum,frame):
#     global MAIN_STOP_FLAG
#     MAIN_STOP_FLAG = True
#     print ("Receive the signal!!",MAIN_STOP_FLAG)
#     sys.exit()
if __name__ == "__main__":
    # signal.signal(signal.SIGINT, signal_handler)
    # signal.signal(signal.SIGTERM, signal_handler)
    # read1 = Read6050(1,"r6050-1","COM7")
    # read1.setDaemon(True)
    # read1.start()
    ser = Read6050(Port='COM7')
    ser.start()
    thread_read = threading.Thread(target=ser.read)
    thread_read.setDaemon(True)
    thread_read.start()
    time.sleep(10)
    ser.stop()
    
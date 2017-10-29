import serial
import sys
import time
import numpy as np
import threading 
import signal
import struct

MAIN_STOP_FLAG = False
class Read6050(threading.Thread):
    def __init__(self,threadID,name,PORT='COM0',baudrate=115200):
        threading.Thread.__init__(self)
        global MAIN_STOP_FLAG
        self.threadID = threadID
        self.name = name
        self.Port = PORT
        self.baudrate = baudrate
        self.ser=serial.Serial(self.Port, self.baudrate, bytesize=8, parity=serial.PARITY_NONE, stopbits=1, timeout=1) 
        self.usRxLength = 0
        self.usLength   = 0
        self.data = np.zeros((3,3),dtype='float16')
        if self.ser.isOpen() is False:
            print ("PORT is not Open!")
            self.ser.close()
            sys.exit()
        self.buff = self.ser.read(0)
    def run(self):
        while True:
            temp = self.ser.read(1)
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
                    self.data = DecodeData(tempBuff)
                    self.buff = self.buff[11:self.usRxLength]
                    self.usRxLength -= 11
            if MAIN_STOP_FLAG is True:
                break
    def __del__(self):
        print ("%s stop!"%(self.name))
        self.ser.close()
def DecodeData(tempBuff,a=np.array([0,0,0],dtype='float16'),\
                w=np.array([0,0,0],dtype='float16'),\
                T=np.array([0],dtype='float16'),
                angle=np.array([0,0,0],dtype='float16')):
    # a=np.array([0,0,0],dtype='float16')
    # w=np.array([0,0,0],dtype='float16')
    # T=np.array([0],dtype='float16')
    # angle=np.array([0,0,0],dtype='float16')
    if (tempBuff[1]==0x51):
        a[0] =  number(tempBuff[2:4])/32768.0*16
        a[1] =  number(tempBuff[4:6])/32768.0*16
        a[2] =  number(tempBuff[6:8])/32768.0*16
        T[0] =  number(tempBuff[8:10])/340.0 + 36.25
        #print ("Xa=%2.3f\tYa=%2.3f\tZa=%2.3f\tT=%3.3f"%(a[0],a[1],a[2],T[0]))
    elif (tempBuff[1]==0x52):
        w[0] =  number(tempBuff[2:4])/32768.0*2000
        w[1] =  number(tempBuff[4:6])/32768.0*2000
        w[2] =  number(tempBuff[6:8])/32768.0*2000
        T[0] =  number(tempBuff[8:10])/340.0 + 36.25
        #print ("Xw=%2.3f\tYw=%2.3f\tZw=%2.3f\tT=%3.3f"%(w[0],w[1],w[2],T[0]))
    elif (tempBuff[1]==0x53):
        angle[0] =  number(tempBuff[2:4])/32768.0*2000
        angle[1] =  number(tempBuff[4:6])/32768.0*2000
        angle[2] =  number(tempBuff[6:8])/32768.0*2000
        T[0] =  number(tempBuff[8:10])/340.0 + 36.25
        #print ("Xangle=%2.3f\tYangle=%2.3f\tZangle=%2.3f\tT=%3.3f"%(angle[0],angle[1],angle[2],T[0]))
    return np.array([a,w,angle],dtype='float16')
def number(buff):
    HL = np.array([0,0],dtype='b')#HighBit LowBit
    SI = np.array([0],dtype='i2') #ShortInt
    HL[0]=buff[1]
    HL[1]=buff[0]
    SI=HL[0]<<8|HL[1]
    return SI
def signal_handler(signum,frame):
    global MAIN_STOP_FLAG
    MAIN_STOP_FLAG = True
    print ("Receive the signal!!",MAIN_STOP_FLAG)
    sys.exit()
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    read1 = Read6050(1,"r6050-1","COM7")
    read1.setDaemon(True)
    read1.start()
    while True:
        time.sleep(0.02)
        print ("data:",read1.data)
    
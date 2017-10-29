import serial
import sys
import time
import numpy as np
import threading 
PORT = "COM7"

## global variable
RxBuff = None
buff   = None
head = {'51':0,'52':0,'53':0}


## global variable
def number(buff):
    HL = np.array([0,0],dtype='b')#HighBit LowBit
    SI = np.array([0],dtype='i2') #ShortInt
    HL[0]=ord(buff[1])
    HL[1]=ord(buff[0])
    SI=HL[0]<<8|HL[1]
    return SI
def DecodeData(tempBuff):
    a=np.array([0,0,0],dtype='float16')
    w=np.array([0,0,0],dtype='float16')
    T=np.array([0],dtype='float16')
    angle=np.array([0,0,0],dtype='float16')
    tempBuff = str(tempBuff)
    if (tempBuff[1]==chr(0x51)):
        a[0] =  number(tempBuff[2:4])/32768.0*16
        a[1] =  number(tempBuff[4:6])/32768.0*16
        a[2] =  number(tempBuff[6:8])/32768.0*16
        T[0] =  number(tempBuff[8:10])/340.0 + 36.25
        print ("Xa=%2.3f\tYa=%2.3f\tZa=%2.3f\tT=%3.3f"%(a[0],a[1],a[2],T[0]))
    elif (tempBuff[1]==chr(0x52)):
        w[0] =  number(tempBuff[2:4])/32768.0*2000
        w[1] =  number(tempBuff[4:6])/32768.0*2000
        w[2] =  number(tempBuff[6:8])/32768.0*2000
        T[0] =  number(tempBuff[8:10])/340.0 + 36.25
        print ("Xw=%2.3f\tYw=%2.3f\tZw=%2.3f\tT=%3.3f"%(w[0],w[1],w[2],T[0]))
    elif (tempBuff[1]==chr(0x53)):
        angle[0] =  number(tempBuff[2:4])/32768.0*2000
        angle[1] =  number(tempBuff[4:6])/32768.0*2000
        angle[2] =  number(tempBuff[6:8])/32768.0*2000
        T[0] =  number(tempBuff[8:10])/340.0 + 36.25
        print ("Xangle=%2.3f\tYangle=%2.3f\tZangle=%2.3f\tT=%3.3f"%(angle[0],angle[1],angle[2],T[0]))
    return np.array([a,w,angle],dtype='float16')
def main():
    ser=serial.Serial(PORT, baudrate=115200, bytesize=8, parity=serial.PARITY_NONE, stopbits=1, timeout=1)
    if ser.isOpen() is False:
        print ("PORT is not Open!")
        ser.close()
        sys.exit()
    usRxLength = 0
    buff = ser.read(0)
    while True:
        temp = ser.read(1)
        buff = buff+temp
        usLength = len(temp)
        #print "buff:",buff.encode('hex')
        if usLength > 0:
            usRxLength = usRxLength+usLength
            while usRxLength >= 11:
                #print "usRxLength:",usRxLength
                tempBuff = buff[:usRxLength]
                #print "tempbuff:",tempBuff.encode('hex')
                if (((tempBuff[0] == chr(0x55))  & \
                    ((tempBuff[1] == chr(0x51)) | \
                     (tempBuff[1] == chr(0x52)) | \
                     (tempBuff[1] == chr(0x53)))) is False ):
                        buff = buff[1:usRxLength]
                        usRxLength = usRxLength - 1
                        continue
                DecodeData(tempBuff)
                buff = buff[11:usRxLength]
                usRxLength -= 11

if __name__ == "__main__":
    main()

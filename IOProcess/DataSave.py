# -*- coding:utf-8 -*-  
import logging
import time
import numpy
import threading

class DataSave:
    def __init__(self,filename):
        self.filename = filename
        self.title = "-----Title-----"
        self.write_buff = ""
        self.fp = None
    def writeTitle(self):
        try:
            fp = open(self.filename,'w')
        except IOError as e:
            logging.error(e)
        try:
            fp.writelines(self.title)
        finally:
            fp.close()
    def setTitle(self,Title):
        self.title = Title + '\n'
    def formatData(self,data,timeCount):
        datatemp = numpy.reshape(data,(1,-1))
        temp = ""
        for i in datatemp[0]:
            temp = temp + "%9.3f,"%(i)
        self.write_buff = "%9.3f"%(timeCount) + ',' + temp + '\n'
    def openFile(self):
        try:
            self.fp = open(self.filename,'a')
        except IOError as e:
            logging.error(e)
    def closeFile(self):
        try:
            self.fp.close()
        except IOError as e:
            logging.error(e)
    def writeData(self):
        try:
            self.fp.writelines(self.write_buff)
        except IOError as e:
            logging.error(e)

class RecordThread(threading.Thread):
    def __init__(self,ser_list):
        threading.Thread.__init__(self)
        self.ser_list=tuple(ser_list)#list of class Read6050
        self.save_list = list()
        self.active = True
        #创建文件并写入title
        for ser in self.ser_list:
            tempName = "./Data/data_" + ser.port + ".csv"
            self.save_list.append(DataSave(tempName))
        try :
            title1 = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            # title2 ="  Time(s)|    ax(g)|    ay(g)|    az(g)|wx(deg/s)|wy(deg/s)|wz(deg/s)|AglX(deg)|AglY(deg)|AglZ(deg)|"
            title2 ="T,ax(g)x,ay(g),az(g),wx(deg/s),wy(deg/s),wz(deg/s),AglX(deg),AglY(deg),AglZ(deg)"
            title = title1 + '\n' + title2
            for save in self.save_list:
                save.setTitle(title)
                save.writeTitle()
        except Exception as e :
            logging.error(e)
    def stop(self):
        self.active = False
    def run(self):
        '''写入数据'''
        time.clock()
        for save in self.save_list:
            save.openFile()
        try :
            while self.active:
                time.sleep(0.02)
                timeCount = time.clock()
                for save,ser in zip(self.save_list,self.ser_list):
                    save.formatData(ser.data,timeCount)
                    save.writeData()
        except Exception as e:
            logging.error(e)
        finally:
            for save in self.save_list:
                save.closeFile()

class RecordThreadToOneFile(threading.Thread):
    def __init__(self,ser_list,savename):
        threading.Thread.__init__(self)
        self.ser_list=tuple(ser_list)#list of class Read6050
        self.save_list = list()
        self.active = True
        timename = time.strftime('%m_%d_%H_%M_%S',time.localtime(time.time()))
        self.filename = "./Data/" + savename + "_" + timename+ '_' + str(len(self.ser_list)) + ".csv"
        self.save = DataSave(self.filename)
        #创建文件并写入title
        try :
            # title1 = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            # title2 ="  Time(s)|    ax(g)|    ay(g)|    az(g)|wx(deg/s)|wy(deg/s)|wz(deg/s)|AglX(deg)|AglY(deg)|AglZ(deg)|"
            title2 ="T,ax(g)x,ay(g),az(g),wx(deg/s),wy(deg/s),wz(deg/s),AglX(deg),AglY(deg),AglZ(deg)"
            titleformat="ax%d,ay%d,az%d,wx%d,wy%d,wz%d,agx%d,agy%d,agz%d"
            title=""
            for i in range(len(self.ser_list)):
                num=(i,)*9
                title+=","+titleformat%num
            title="T"+title
            self.save.setTitle(title)
            self.save.writeTitle()
        except Exception as e :
            logging.error(e)
    def stop(self):
        self.active = False
    def run(self):
        '''写入数据'''
        startime=time.clock()
        self.save.openFile()
        try :
            while self.active:
                time.sleep(0.02)
                timeCount = time.clock() - startime
                data=[]
                for ser in self.ser_list:
                    data+=list(numpy.reshape(ser.data,(1,-1)))
                self.save.formatData(data,timeCount)
                self.save.writeData()
        except Exception as e:
            logging.error(e)
        finally:
            self.save.closeFile()
            # logging.debug("exit run in recordThread del")

        

        
if __name__ ==  '__main__':
    title1 = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    # title2 = "Time(s) |ax(g)|ay(g)|az(g)|wx(deg/s)|wy(deg/s)|wz(deg/s)|AngleX(deg)|AngleY(deg)|AngleZ(deg)"
    title2 ="T,ax(g)x,ay(g),az(g),wx(deg/s),wy(deg/s),wz(deg/s),AglX(deg),AglY(deg),AglZ(deg)"
    title = title1 + '\n' + title2
    print (title)
    save = DataSave("./Test/test.txt")
    save.setTitle(title)
    save.writeTitle()
    data = numpy.random.rand(3,3)
    time.clock()
    save.openFile()
    try:
        for i in range(20):
            time.sleep(0.05)
            timeCount = time.clock()
            save.formatData(data,timeCount)
            save.writeData()
    except Exception as e:
        logging.error(e)
    finally:
        save.closeFile()

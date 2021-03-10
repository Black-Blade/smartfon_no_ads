#!/usr/bin/env python3
#/***************************************************************************//**
#@file			dropdns.py
#								
#@author		Black-Blade 
#@brief			dropdns.py 
#@date    		27.01.2021
#@version		0.0.1 Doxygen style eingebaut und erstellen dieser File
#@see           https://tools.ietf.org/html/rfc1035
#*******************************************************************************/

import logging
import binascii
import sqlite3

# IMPORT MY STANDRT CLASS
from config import Config

if __name__ == "__main__":
    quit()

class DNS_DROP:
#/*******************************************************************************
# @author       Black-Blade
# @brief        Constructor of DNS_DROP
# @date         10.03.2021
# @param        [piholeenabel(True,False), piholegrvotydb(True,False),listenabel,listfile,buffertimeout(int)]  
# @return       
# @version      0.0.1 Doxygen style eingebaut und erstellen dieser File
# @see          
# *******************************************************************************/
    def __init__(self,dorpserver=None):
            logging.debug ("")
            if dorpserver is None:
                self._pihole_enabel=Config.DROPPYHOLEENABLE
                self._db = Config.DROPPYHOLEGRAVITYDB
                self._list_enabel=Config.DROPLISTENABLE
                self._list =Config.DROPLISTFILE
                self._droptimerdnsbuffer =Config.DROPTIMEDNSBUFFER.to_bytes(4, byteorder="big")
            else:
                piholeenabel, piholegrvotydb,listenabel,listfile,buffertimeout = dorpserver
                self._pihole_enabel=piholeenabel
                self._db = piholegrvotydb
                self._list_enabel=listenabel
                self._list =listfile
                self._droptimerdnsbuffer =buffertimeout.to_bytes(4, byteorder="big")

#/*******************************************************************************
# @author       Black-Blade
# @brief        Deconstructor of DNS_DROP
# @date         06.03.2021
# @param        
# @return       
# @version      0.0.1 Doxygen style eingebaut und erstellen dieser File
# @see          
# *******************************************************************************/
    def __del__(self): 
        logging.debug ("")

#/*******************************************************************************
# @author       Black-Blade
# @brief        read the name of the request domain
# @date         06.03.2021
# @param        [data,dnsdatapointer,re]
# @return       [name(nane)]
# @version      0.0.1 Doxygen style eingebaut und erstellen dieser File
# @see          https://tools.ietf.org/html/rfc1035          
# *******************************************************************************/
    def _namepaser(self,data,dnsdatapointer,re=0):
        logging.debug ("")
        name =""
        conter =0
        cd=False #/False Conter /True Data
        
        while True:
            if data [dnsdatapointer] &0xC0 ==0xC0:
                tempdatapointer= data[dnsdatapointer+1]  | (data[dnsdatapointer] & 0x3f) << 8
                logging.debug ("pointer         : "+str(re))
                logging.debug ("pointerdata     : "+str(tempdatapointer))
        
                dnsdatapointer=dnsdatapointer+2
                tempdatapointer,tempname = self._namepaser(data,tempdatapointer,re+1)
                name=name+tempname
                break

            if (data [dnsdatapointer])==0 and cd == False:
                dnsdatapointer=dnsdatapointer+1
                break
     

            if  cd == False:
                conter= data [dnsdatapointer]
                dnsdatapointer=dnsdatapointer+1
                cd=True
                continue
            else:
                name=name + data[dnsdatapointer:dnsdatapointer+conter].decode()
                dnsdatapointer=dnsdatapointer+conter
                name=name+"."
                cd=False
                continue   
        
        if re==0:
            name =name[0:-1] 
        return [dnsdatapointer,name]

#/*******************************************************************************
# @author       Black-Blade
# @brief        test domain in the gravity list of PYHOLE
# @date         06.03.2021
# @param        [domain]
# @return       [isblock,blockname,dname]
# @version      0.0.1 Doxygen style eingebaut und erstellen dieser File
# @see        
# *******************************************************************************/
    def _search_db(self,domain):
        db = sqlite3.connect(self._db)
        db.cursor()
        
        found = False
        for name in db.execute("SELECT domain FROM gravity WHERE domain LIKE '"+domain+"'"):
            found = True
            break
        
        db.close()
        
        if found == True:
            return [True,"PIHOLE",name[0]]
        return [False,"OK",domain]

#/*******************************************************************************
# @author       Black-Blade
# @brief        test domain in the list 
# @date         06.03.2021
# @param        [domain]
# @return       [isblock,blockname,dname]
# @version      0.0.1 Doxygen style eingebaut und erstellen dieser File
# @see        
# *******************************************************************************/
    def _search_list(self,domain):
        found = False 
        with open(self._list) as file_in:
            for line in file_in:
                if line[0] =="#":
                    continue
                line= line.replace("\r","")
                line= line.replace("\n","")
                if domain.find(line) >=0 :
                    found = True
                    break
        if found == True:
            return [True,"LIST",line]
        return [False,"OK",domain]
#/*******************************************************************************
# @author       Black-Blade
# @brief        drop domain (send a 0.0.0.0 resonse to the cleint) 
# @date         06.03.2021
# @param        [data]
# @return       [isblock,blockname,dname]
# @version      0.0.1 Doxygen style eingebaut und erstellen dieser File
# @see          https://tools.ietf.org/html/rfc1035        
# *******************************************************************************/       
    def drop(self,data):
        logging.debug ("")
        
        dnsdatapointer =0
        rxdata=b''
        isblock =False
        blockname="OK"

        #copy transaktion id
        rxdata =rxdata + data[dnsdatapointer:dnsdatapointer+2]
        dnsdatapointer= dnsdatapointer+2
        
        # set standart falg
        rxdata =rxdata +bytearray(b'\x85\x80')
        dnsdatapointer= dnsdatapointer+2
     
        #read datablocks(RR)
        question        = data[dnsdatapointer+1]  | data[dnsdatapointer] << 8

        # test question is 0 then no data back
        if question ==0:
            return None

        
        # set the datapointer
        dnsdatapointer= dnsdatapointer+8

        # set rxdata  Question (1)
        rxdata =rxdata +bytearray(b'\x00\x01')
        
        # set rxdata  Answer (1)
        rxdata =rxdata +bytearray(b'\x00\x01')
        
        # set rxdata  Authority (0)
        rxdata =rxdata +bytearray(b'\x00\x00')
        
        # set rxdata  Additional (0)
        rxdata =rxdata +bytearray(b'\x00\x00')

        
        #Read the Domainname from data
        sdata= dnsdatapointer
        dnsdatapointer,name = self._namepaser(data,dnsdatapointer)
        rxdata=rxdata+ data[sdata:dnsdatapointer]  
        
        # Test Domain 
        if self._list_enabel ==True and isblock== False:
            isblock,blockname,dname = self._search_list(name)
    
        if self._pihole_enabel ==True and isblock== False:
            isblock,blockname,dname= self._search_db(name)

        if isblock== False:
            return [isblock,rxdata,blockname,name] 
  
        # Read the Type 
        btyte=data[dnsdatapointer:dnsdatapointer+2]
        htype= data[dnsdatapointer+1]  | data[dnsdatapointer] << 8
        sdata= dnsdatapointer
        dnsdatapointer=dnsdatapointer+2
        rxdata=rxdata+ data[sdata:dnsdatapointer]  

        # Read the Class
        bcass=data[dnsdatapointer:dnsdatapointer+2]
        sdata= dnsdatapointer
        dnsdatapointer=dnsdatapointer+2
        rxdata=rxdata+ data[sdata:dnsdatapointer]  

        #pointer of name
        rxdata =rxdata +bytearray(b'\xC0\x0C')
        
        rxdata =rxdata +btyte 
        rxdata =rxdata +bcass
        
        rxdata =rxdata +bytearray(self._droptimerdnsbuffer)
        
        if htype==1:
            rxdata =rxdata +bytearray(b'\x00\x04')
            rxdata =rxdata +bytearray(b'\x00\x00\x00\x00')
        elif htype==2:
            rxdata =rxdata +bytearray(b'\x00\x04')
            rxdata =rxdata +bytearray(b'\x00\x00\x00\x00')
        elif htype==5:
            rxdata =rxdata +bytearray(b'\x00\x04')
            rxdata =rxdata +bytearray(b'\x00\x00\x00\x00')
        elif htype==6:
            rxdata =rxdata +bytearray(b'\x00\x04')
            rxdata =rxdata +bytearray(b'\x00\x00\x00\x00')
        elif htype==16:
            rxdata =rxdata +bytearray(b'\x00\x04')
            rxdata =rxdata +bytearray(b'\x00\x00\x00\x00')
        elif htype==28:
            rxdata =rxdata +bytearray(b'\x00\x10')
            rxdata =rxdata +bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        elif htype==41:
            rxdata =rxdata +bytearray(b'\x00\x04')
            rxdata =rxdata +bytearray(b'\x00\x00\x00\x00')
        else:
            rxdata =rxdata +bytearray(b'\x00\x04')
            rxdata =rxdata +bytearray(b'\x00\x00\x00\x00')


        return [isblock,rxdata,blockname,dname]
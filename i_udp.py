#!/usr/bin/env python3
#/***************************************************************************//**
# @file			i_udp.py
#								
# @author		Black-Blade 
# @brief		i_udp.py 
# @date    		13.01.2021
# @version		0.0.1 Doxygen style eingebaut und erstellen dieser File
# @see          https://tools.ietf.org/html/rfc1035
#*******************************************************************************/

import socket
from socket import AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET, SHUT_RDWR
from _thread import start_new_thread

# IMPORT MY STANDRT CLASS
from log import logging
from config import Config


if __name__ == "__main__":
    quit()

class Input_UDP:
#/*******************************************************************************
# @author       Black-Blade
# @brief        Constructor of Input_UDP
# @date         10.03.2021
# @param        switch(pointer),geoip(pointer),[UDPSERVER(String),UDPPORT(INT)]
# @return       
# @version      0.0.1 Doxygen style eingebaut und erstellen dieser File
# @see          
# *******************************************************************************/
    def __init__(self,switch,geoip,udpserver=None):
        logging.debug ("")

        self._switch =switch
        self._geoip=geoip
        if udpserver is None:
            self._listen_addr = Config.I_DOTSERVER
            self._listen_port = Config.I_UDPPORT
        else:
            server,port =udpserver
            self._listen_addr = server
            self._listen_port = port

        self._buffersize =1024

        self._conterrequests=0
        self._conterrequest=0
        self._countererror =0

#/*******************************************************************************
# @author       Black-Blade
# @brief        Deconstructor of Input_UDP
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
# @brief        Init of Input_UDP
# @date         06.03.2021
# @param        
# @return       
# @version      0.0.1 Doxygen style eingebaut und erstellen dieser File
# @see          
# *******************************************************************************/
    def init(self):
        logging.debug ("")
        start_new_thread(self._init_thread,())

#/*******************************************************************************
# @author       Black-Blade
# @brief        Init the thread of Input_UDP
# @date         06.03.2021
# @param        
# @return       
# @version      0.0.1 Doxygen style eingebaut und erstellen dieser File
# @see          https://tools.ietf.org/html/rfc1035
# *******************************************************************************/
    def _init_thread(self):
        logging.debug ("")
        with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as sock:
            sock.bind((self._listen_addr, self._listen_port))
            logging.info ("UDP input start from :"+str( self._listen_addr)+":"+str( self._listen_port))
            while True:
                try:
                    msg,conn = sock.recvfrom(self._buffersize)
                    start_new_thread(self._decoder_thread,(sock,conn, msg))
                except OSError as err:
                    logging.error("OS error: {0}".format(err))

#/*******************************************************************************
# @author       Black-Blade
# @brief        Read the DNS rquest of extern
# @date         10.03.2021
# @param        conn,addr    
# @return       
# @version      0.0.1 Doxygen style eingebaut und erstellen dieser File
# @see          https://tools.ietf.org/html/rfc1035
# *******************************************************************************/
    def _decoder_thread(self,sock,conn, txdata):
        try:
            logging.debug ("")
            host, port = conn
        
            if  self._geoip is None:
                ok= True
                text= "NO GEOIP"
            else:
                ok,text =  self._geoip(host)
            
            if ok == True:
                self._conterrequests=self._conterrequests+1
                self._conterrequest=self._conterrequest+1
 
                data =self._switch(txdata)
                if data is not None:
                    isblock,rxdata,blockname,dname = data
                    sock.sendto(rxdata , conn)
                    logging.info("IP : "+str(host)+":"+str(port)+" :"+ text)
                    if isblock==True:
                        logging.info("Domain : "+str(dname)+ " is block true : blockname " + str(blockname)) 
                    else:
                        logging.info("Domain : "+str(dname)+ " is block false ") 
            else:
                logging.info("IP : "+str(host)+": "+ text)
        
        except OSError as err:
            logging.error("OS error: {0}".format(err))
            self._countererror=self._countererror +1
        self._conterrequest=self._conterrequest-1

#/*******************************************************************************
# @author       Black-Blade
# @brief        Logs REQUESTS
# @date         08.03.2021
# @param        
# @return       
# @version      0.0.1 Doxygen style eingebaut und erstellen dieser File
# @see     
# *******************************************************************************/
    def logs(self):
        logging.info("REQUEST : "+str(self._conterrequest) +": REQUESTS : "+str(self._conterrequests)+": ERRORS : "+str(self._countererror)) 
                   
#!/usr/bin/env python3
#/***************************************************************************//**
# @file			i_tcp.py
#								
# @author		Black-Blade 
# @brief		i_tcp.py 
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

class Input_TCP:
#/*******************************************************************************
# @author       Black-Blade
# @brief        Constructor of Input_TCP
# @date         08.03.2021
# @param        [switch(pointer),geoip(pointer)]
# @return       
# @version      0.0.1 Doxygen style eingebaut und erstellen dieser File
# @see          
# *******************************************************************************/
    def __init__(self,switch,geoip):
        logging.debug ("")

        self._switch =switch
        self._geoip=geoip

        self._listen_addr = Config.I_TCPSERVER
        self._listen_port = Config.I_TCPPORT
        self._timeout = Config.I_TCPTIMEOUT
        
        self._maxlisten =100
        self._buffersize =1024
       
        self._conterrequests=0
        self._conterrequest=0
        self._countererror =0


#/*******************************************************************************
# @author       Black-Blade
# @brief        Deconstructor of Input_TCP
# @date         08.03.2021
# @param        
# @return       
# @version      0.0.1 Doxygen style eingebaut und erstellen dieser File
# @see          
# *******************************************************************************/
    def __del__(self): 
        logging.debug ("")

#/*******************************************************************************
# @author       Black-Blade
# @brief        Init of Input_TCP
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
# @brief        Init the thread of Input_TCP
# @date         08.03.2021
# @param        
# @return       
# @version      0.0.1 Doxygen style eingebaut und erstellen dieser File
# @see          https://tools.ietf.org/html/rfc1035
# *******************************************************************************/
    def _init_thread(self):
        logging.debug ("")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((self._listen_addr, self._listen_port))
            logging.info ("TCP input start from :"+str( self._listen_addr)+":"+str( self._listen_port))
       
            sock.listen(self._maxlisten)
            while True:
                try:
                    conn, addr = sock.accept()
                    start_new_thread(self._decoder_thread,(conn, addr))
                except OSError as err:
                    logging.error("OS error: {0}".format(err))

#/*******************************************************************************
# @author       Black-Blade
# @brief        Read the DNS rquest of extern
# @date         08.03.2021
# @param        
# @return       
# @version      0.0.1 Doxygen style eingebaut und erstellen dieser File
# @see          https://tools.ietf.org/html/rfc1035   
# *******************************************************************************/    
    def _decoder_thread(self,conn, addr):
        logging.debug ("")
        try:
            conn.settimeout(self._timeout)   
            host, port = addr

            ok,text =  self._geoip(host)
            if ok == True:
           
                self._conterrequests=self._conterrequests+1
                self._conterrequest=self._conterrequest+1
 
                txdata =  conn.recv(self._buffersize)
            
                # clear the first 2 byte for datalen
                txdata =txdata[2:]
                
                data =self._switch(txdata)
                if data is not None:
                    isblock,rxdata,blockname,dname = data
                # Add 2 byte for len for tcp protokll
                    rxdata= (len(rxdata)).to_bytes(2, byteorder="big") + rxdata

                    conn.send(rxdata)
                    logging.info("IP : "+str(host)+":"+str(port)+" :"+ text)
                    if isblock==True:
                        logging.info("Domain : "+str(dname)+ " is block true : blockname " + str(blockname)) 
                    else:
                        logging.info("Domain : "+str(dname)+ " is block false ") 

            else:
                logging.info("IP : "+str(host)+": "+ text)
            conn.close()

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
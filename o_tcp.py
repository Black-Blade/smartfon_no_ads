#!/usr/bin/env python3
#/***************************************************************************//**
#@file			o_tcp.py
#								
#@author		Black-Blade 
#@brief			o_tcp.py 
#@date    		13.01.2021
#@version		0.0.1 Doxygen style eingebaut und erstellen dieser File
#@see           https://tools.ietf.org/html/rfc1035

#*******************************************************************************/
import socket

# IMPORT MY STANDRT CLASS
from log import logging
from config import Config

if __name__ == "__main__":
    quit()

class OUTPUT_TCP:
#/*******************************************************************************
# @author       Black-Blade
# @brief        Constructor of OUTPUT_TCP
# @date         06.03.2021
# @param        
# @return       
# @version      0.0.1 Doxygen style eingebaut und erstellen dieser File
# @see          
# *******************************************************************************/
    def __init__(self):
        logging.debug ("")
        self._ip=Config.O_TCPSERVER
        self._port=Config.O_TCPPORT
        self._settimeout =Config.O_TCPTIMEOUT
        self._buffersize =1024
       
#/*******************************************************************************
# @author       Black-Blade
# @brief        Deconstructor of OUTPUT_TCP
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
# @brief        Send data to extern DNS TCP server
# @date         06.03.2021
# @param        [txdata (data to dns server)]
# @return       [rxdata (data from dns server)]
# @version      0.0.1 Doxygen style eingebaut und erstellen dieser File
##@see          https://tools.ietf.org/html/rfc1035          
# *******************************************************************************/
    def send(self,txdata):
        logging.debug ("")

        rxdata =None
        
        try:
            #Add 2 byte for len for tcp protokll
            txdata= (len(txdata)).to_bytes(2, byteorder="big") + txdata
    
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self._settimeout)
    
            s.connect((self._ip, self._port))

            logging.debug ("TCP output send to :"+str( self._ip)+":"+str( self._port))
            s.send(txdata)
            rxdata = s.recv(self._buffersize) 
            logging.debug ("TCP incomming fom :"+str( self._ip)+":"+str( self._port))
       

            s.close()

            # clear the first 2 byte for datalen
            rxdata =rxdata[2:]
        
        except OSError as err:
            logging.error("OS error: {0}".format(err))
        
        return rxdata
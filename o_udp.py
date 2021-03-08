#!/usr/bin/env python3
#/***************************************************************************//**
#@file			o_udp.py
#								
#@author	    Black-Blade 
#@brief			o_udp.py 
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

class OUTPUT_UDP:
#/*******************************************************************************
# @author       Black-Blade
# @brief        Constructor of OUTPUT_UDP
# @date         06.03.2021
# @param        
# @return       
# @version      0.0.1 Doxygen style eingebaut und erstellen dieser File
# @see          
# *******************************************************************************/
    def __init__(self):
        logging.debug ("")

        self._ip=Config.O_UDPSERVER
        self._port=Config.O_UDPPORT
        self._buffersize =1024

#/*******************************************************************************
# @author       Black-Blade
# @brief        Deconstructor of OUTPUT_UDP
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
# @brief        Send data to extern DNS UDP server
# @date         06.03.2021
# @param        [txdata (data to dns server)]
# @return       [rxdata (data from dns server)]
# @version      0.0.1 Doxygen style eingebaut und erstellen dieser File
#@see           https://tools.ietf.org/html/rfc1035         
# *******************************************************************************/
    def send(self,txdata):
        logging.debug ("")
        rxdata =None
        
        try:

            s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            s.connect((self._ip, self._port))
            logging.debug ("UDP output send to :"+str( self._ip)+":"+str( self._port))
            
            s.send(txdata)
            rxdata = s.recv(self._buffersize) 
            logging.debug ("UDP incomming fom :"+str( self._ip)+":"+str( self._port))
       
            s.close()
        except OSError as err:
            logging.error("OS error: {0}".format(err))

        return rxdata
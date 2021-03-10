#!/usr/bin/env python3
#/***************************************************************************//**
# @file			o_dot.py
#								
# @author		Black-Blade 
# @brief		o_dot.py 
# @date    		15.01.2021
# @version		0.0.1 Doxygen style eingebaut und erstellen dieser File
# @see          https://github.com/melvilgit/DNS-OVER-TLS/blob/master/App.py
#               https://tools.ietf.org/html/rfc7858
#*******************************************************************************/

import socket
from socket import AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET, SHUT_RDWR
import ssl
import threading

# IMPORT MY STANDRT CLASS
from log import logging
from config import Config

if __name__ == "__main__":
    quit()

class OUTPUT_DOT:
#/*******************************************************************************
# @author       Black-Blade
# @brief        Constructor of OUTPUT_DOT
# @date         10.03.2021
# @param        [dohserver(String(),timeout(fload)]      
# @return       
# @version      0.0.1 Doxygen style eingebaut und erstellen dieser File
# @see          
# *******************************************************************************/
    def __init__(self,dotserver=None):
        logging.debug ("")
        if dotserver is None:
            server= Config.O_DOTSERVER
            self._settimeout =Config.O_DOTTIMEOUT
        else:
            server,timeout = dotserver
            self._settimeout= timeout
            
        self._port=853
        self._buffersize =1024
        
        if server=="cloudflare":
            #self._ip="1dot1dot1dot1.cloudflare-dns.com"
            self._ip="1.1.1.1"

        if server=="cleanbrowsing-family-1":
            #self._ip="family-filter-dns.cleanbrowsing.org"
            self.ip="185.228.168.168"

        if server=="cleanbrowsing-family-2":
            #self._ip="family-filter-dns.cleanbrowsing.org"
            self.ip="185.228.169.168"

        if server=="cleanbrowsing-adult-1":
            #self._ip="adult-filter-dns.cleanbrowsing.org"
            self._ip="185.228.168.10"
        if server=="cleanbrowsing-adult-2":
            #self._ip="adult-filter-dns.cleanbrowsing.org"
            self._ip="185.228.169.10"
        
        if server=="security-adult-1":
            #self._ip="security-filter-dns.cleanbrowsing.org"
            self._ip="185.228.168.9"
        if server=="security-adult-2":
            #self._ip="security-filter-dns.cleanbrowsing.org"
            self._ip="185.228.169.9"
        
        if server=="ffmuc":
            #self._ip="dot.ffmuc.net"
            self._ip="5.1.66.255"

        if server=="googel-1":
            #self._ip="dns.google"
            self._ip="8.8.8.8"

        if server=="googel-1":
            #self._ip="dns.google"
            self._ip="8.8.4.4"

        if server=="digitale-gesellschaft":
            #self._ip="dns.digitale-gesellschaft.ch"
            self._ip="185.95.218.42"

        if server=="quad9":
            #self._ip="dns.quad9.net"
            self.ip="9.9.9.9"

        if server=="dismail-1":
            #self._ip="fdns1.dismail.de"
            self._ip="80.241.218.68"

        if server=="dismail-2":
            self._ip="fdns2.dismail.de"
            self._ip="159.69.114.157"
            
        if server=="digitalcourage":
            #self._ip="dns3.digitalcourage.de"
            self._ip="46.182.19.48"
#/*******************************************************************************
# @author       Black-Blade
# @brief        Deconstructor of OUTPUT_DOT
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
# @brief        Send data to extern DNS DOT server
# @date         06.03.2021
# @param        [txdata (data to dns server)]
# @return       [rxdata (data from dns server)]
# @version      0.0.1 Doxygen style eingebaut und erstellen dieser File
# @see          https://tools.ietf.org/html/rfc7858        
# *******************************************************************************/

    def send(self,txdata):
        logging.debug ("")
        
        rxdata =None
        try:

            #Add 2 byte for len for tcp protokll
            txdata= (len(txdata)).to_bytes(2, byteorder="big") + txdata
   
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self._settimeout)

            context = ssl.create_default_context()
            #context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            #context.load_verify_locations('./ca-certificate.crt')

            s = context.wrap_socket(sock, server_hostname=self._ip)

    
            # CONNECT AND PRINT REPLY
            s.connect((self._ip, self._port))
        

            logging.debug ("DOT output send to :"+str( self._ip)+":"+str( self._port))
            s.send(txdata)
            rxdata = s.recv(self._buffersize) 
            logging.debug ("DOT incomming fom :"+str( self._ip)+":"+str( self._port))
       

            s.close()

            # clear the first 2 byte for datalen
            rxdata =rxdata[2:]
      
        except OSError as err:
            logging.error("OS error: {0}".format(err))
      
        return rxdata
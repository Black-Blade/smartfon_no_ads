#!/usr/bin/env python3
#/***************************************************************************//**
# @file			o_doh.py
#								
# @author		Black-Blade 
# @brief		o_doh.py 
# @date    		17.01.2021
# @version		0.0.1 Doxygen style eingebaut und erstellen dieser File
# @see          https://tools.ietf.org/html/rfc8484
#*******************************************************************************/
#pip3 install requests

import urllib3
import base64
from urllib.request import urlretrieve
from urllib.parse import quote

# IMPORT MY STANDRT CLASS
from log import logging
from config import Config

if __name__ == "__main__":
    quit()

class OUTPUT_DOH:
#/*******************************************************************************
# @author       Black-Blade
# @brief        Constructor of OUTPUT_DOH
# @date         06.03.2021
# @param        
# @return       
# @version      0.0.1 Doxygen style eingebaut und erstellen dieser File
# @see          
# *******************************************************************************/
    def __init__(self):
        logging.debug ("")
        server = Config.O_DOHSERVER

        if server=="cloudflare-dns-post":
            self._url       ="https://cloudflare-dns.com/dns-query"
            self._method    ="POST"
            self._base64    =False
            self._headers={
                    'Accept': 'application/dns-udpwireformat',
                    'Content-type': 'application/dns-udpwireformat'
                    }
        
        if server=="cloudflare-dns-get":
            self._url=      "https://cloudflare-dns.com/dns-query?ct=application/dns-udpwireformat&dns="
            self._method    ="GET"
            self._base64    =True
            self._headers={
                    'Accept': 'application/dns-udpwireformat',
                    'Content-type': 'application/dns-udpwireformat'
                    }
        
        if server=="cleanbrowsing-family-get":
            self._url ="https://doh.cleanbrowsing.org/doh/family-filter/?ct&dns="
            self._method="GET"
            self._base64=True
            self._headers={
                    'Accept': 'application/dns-udpwireformat',
                    'Content-type': 'application/dns-udpwireformat'
                    }
        if server=="cleanbrowsing-adult-get":
            self._url ="https://doh.cleanbrowsing.org/doh/adult-filter/?ct&dns="
            self._method="GET"
            self._base64=True
            self._headers={
                    'Accept': 'application/dns-udpwireformat',
                    'Content-type': 'application/dns-udpwireformat'
                    }
        if server=="cleanbrowsing-security-get":
            self._url ="https://doh.cleanbrowsing.org/doh/security-filter/?ct&dns="
            self._method="GET"
            self._base64=True
            self._headers={
                    'Accept': 'application/dns-udpwireformat',
                    'Content-type': 'application/dns-udpwireformat'
                    }
        if server=="ffmuc-post":
            self._url ="https://doh.ffmuc.net/dns-query"
            self._method="POST"
            self._base64=False
            self._headers={
                    'Accept': 'application/dns-udpwireformat',
                    'Content-type': 'application/dns-udpwireformat'
                    }
        
        if server=="google-post":
            self._url ="https://dns.google/dns-query"
            self._method="POST"
            self._base64=False
            self._headers = {
                    'Accept': 'application/dns-message',
                    'Content-type': 'application/dns-message'
                    }

        if server=="google-get":
            self._url ="https://dns.google/dns-query?ct/?ct&dns="
            self._method="GET"
            self._base64=True
            self._headers = {
                    'Accept': 'application/dns-message',
                    'Content-type': 'application/dns-message'
                    }
        if server=="digitale-gesellschaft-post":
            self._url ="https://dns.digitale-gesellschaft.ch/dns-query"
            self._method="POST"
            self._base64=False
            self._headers = {
                    'Accept': 'application/dns-udpwireformat',
                    'Content-type': 'application/dns-udpwireformat'
                    }

#/*******************************************************************************
# @author       Black-Blade
# @brief        Deconstructor of OUTPUT_DOH
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
# @brief        Send data to extern DNS DOH server
# @date         06.03.2021
# @param        [txdata (data to dns server)]
# @return       [rxdata (data from dns server)]
# @version      0.0.1 Doxygen style eingebaut und erstellen dieser File
# @see          https://tools.ietf.org/html/rfc8484        
# *******************************************************************************/
    def send(self,txdata):
        logging.debug ("")

        rxdata =None
        r= None
        #Add 4 byte for DOH PROTOKOLL
        transactionid= txdata[0:2]
        txdata = b'\xab\xcd\x01\x00' +txdata[4:]
        
        if self._base64==True:
            txdata = base64.b64encode(txdata).decode("utf-8") 
            txdata = txdata.replace("=", "")
            txdata = quote(txdata)

        try:
        
            http = urllib3.PoolManager()
            if self._method=="POST":
                r = http.request(self._method, self._url,
                    headers=self._headers,
                    body=txdata)

            if self._method=="GET":
                url= self._url+ txdata
                r = http.request(self._method,url,
                    headers=self._headers)

            if r.status == 200:
                
                # clear the first 2 byte for DOH PROTOKLL
                rxdata =r.data[2:]
                rxdata = transactionid+rxdata
            
            http.clear()
        except OSError as err:
            logging.error("OS error: {0}".format(err))
        
        return rxdata
    

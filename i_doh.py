#!/usr/bin/env python3
#/***************************************************************************//**
# @file			i_doh.py
#								
# @author		Black-Blade 
# @brief		i_doh.py 
# @date    		21.1.2021
# @version		0.0.1 Doxygen style eingebaut und erstellen dieser File
# @see          https://tools.ietf.org/html/rfc8484
#*******************************************************************************/

from http.server import BaseHTTPRequestHandler, HTTPServer
from _thread import start_new_thread
import ssl

# IMPORT MY STANDRT CLASS
from log import logging
from config import Config

if __name__ == "__main__":
    quit()

g_dot_geoip=None
g_dot_switch=None
g_dot_path=""
g_conterrequests=0
g_conterrequest=0
g_countererror =0

class Webserver(BaseHTTPRequestHandler):
#/*******************************************************************************
# @author       Black-Blade
# @brief        set resonse
# @date         06.03.2021
# @param        
# @return       
# @version      0.0.1 Doxygen style eingebaut und erstellen dieser File
# @see          
# *******************************************************************************
    def _set_response(self,code):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
#/*******************************************************************************
# @author       Black-Blade
# @brief        GET requst
# @date         06.03.2021
# @param        
# @return       
# @version      0.0.1 Doxygen style eingebaut und erstellen dieser File
# @see          
# *******************************************************************************
    def do_GET(self):
        global g_countererror
        host, port = self.client_address
        ok,text= g_dot_geoip(host)
        logging.info("IP : "+str(host)+":"+str(port)+" :"+ text)           
        if ok == True:
            logging.debug("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
            self._set_response(404)
            logging.info("IP : "+str(host)+": "+ "404")
            g_countererror=g_countererror +1
        else:
            self._set_response(403)
            logging.info("IP : "+str(host)+": "+ text)
            g_countererror=g_countererror +1
#/*******************************************************************************
# @author       Black-Blade
# @brief        POST requst
# @date         06.03.2021
# @param        
# @return       
# @version      0.0.1 Doxygen style eingebaut und erstellen dieser File
# @see          
# *******************************************************************************
    def do_POST(self):
        global g_conterrequests
        global g_conterrequest
        global g_countererror
        host, port = self.client_address
        
        if  g_dot_geoip is None:
            ok= True
            text= "NO GEOIP"
        else:
            ok,text =  g_dot_geoip(host)

        if ok==True:
           if self.path==g_dot_path:
                accept = self.headers['Accept'] 
                content_type = self.headers['Content-Type'] 
                content_length = int(self.headers['Content-Length'])
                if accept=="application/dns-message":
                    post_data = self.rfile.read(content_length) 
                    data = g_dot_switch(post_data)
                    if data is not None:
                        g_conterrequests=g_conterrequests+1
                        g_conterrequest=g_conterrequest+1
                        isblock,rxdata,blockname,dname = data
                        self.send_response(200)
                        self.send_header('Content-type', content_type)
                        self.end_headers()
                        self.wfile.write(rxdata)
                        logging.info("IP : "+str(host)+":"+str(port)+" :"+ text)
                        if isblock==True:
                            logging.info("Domain : "+str(dname)+ " is block true : blockname " + str(blockname)) 
                        else:
                            logging.info("Domain : "+str(dname)+ " is block false ") 
                    else:
                        self._set_response(500)
                        logging.info("IP : "+str(host)+":"+str(port)+": "+ "500")
                        g_countererror=g_countererror +1
                else:
                    self._set_response(404)
                    logging.info("IP : "+str(host)+":"+str(port)+": "+ "404")
                    g_countererror=g_countererror +1
        else:
            self._set_response(403)
            logging.info("IP : "+str(host)+":"+str(port)+": "+ text)
            g_countererror=g_countererror +1
        g_conterrequest=g_conterrequest-1
                
class Input_DOH:
#/*******************************************************************************
# @author       Black-Blade
# @brief        Constructor of Input_DOT
# @date         10.03.2021
# @param        switch(pointer),geoip(pointer),[DOHPATH(String),DOHSERVER(String),DOHPORT(INT),CERTFILE,CERTPKEY]
# @return       
# @version      0.0.1 Doxygen style eingebaut und erstellen dieser File
# @see          
# *******************************************************************************/
 
    def __init__(self,switch,geoip,dohserver = None):
        logging.debug ("")

        global g_dot_geoip
        global g_dot_switch
        global g_dot_path

        g_dot_geoip = geoip
        g_dot_switch = switch

        if dohserver is None:
            g_dot_path =Config.I_DOHPATH
    
            self._listen_addr = Config.I_DOHSERVER
            self._listen_port = Config.I_DOHPORT
            
            self._server_cert = Config.CERTFILE
            self._server_key = Config.CERTPKEY
        else:
            path,server,port,cfile,ckey =dohserver
            g_dot_path =path
    
            self._listen_addr = server
            self._listen_port = port
            
            self._server_cert = cfile
            self._server_key = ckey

#/*******************************************************************************
# @author       Black-Blade
# @brief        Deconstructor of Input_DOH
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
# @brief        Init of Input_DOH
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
# @brief        Init the thread of Input_DOH
# @date         06.03.2021
# @param        
# @return       
# @version      0.0.1 Doxygen style eingebaut und erstellen dieser File
# @see          https://tools.ietf.org/html/rfc1035
#               https://tools.ietf.org/html/rfc8484     
# *******************************************************************************/
    def _init_thread(self):
        logging.debug ("")
        server_address = (self._listen_addr, self._listen_port)
        httpd = HTTPServer(server_address, Webserver)
        httpd.socket = ssl.wrap_socket (httpd.socket, certfile=self._server_cert ,keyfile=self._server_key, server_side=True)
        logging.info ("DOH input start from :"+str( self._listen_addr)+":"+str( self._listen_port))
       
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        logging.error('Stopping httpd...\n')
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
        global g_conterrequests
        global g_conterrequest
        global g_countererror
        logging.info("REQUEST : "+str(g_conterrequest) +": REQUESTS : "+str(g_conterrequests)+": ERRORS : "+str(g_countererror)) 
                      
    
#!/usr/bin/env python3
#/***************************************************************************//**
#	@file					main.py
#								
#	@author				Black-Blade 
#	@brief				log.py 
#	@date    			13.1.2021
#	@version			0.0.1 Doxygen style eingebaut und erstellen dieser File
# @see          https://tools.ietf.org/html/rfc1035
#               https://tools.ietf.org/html/rfc7858
#               https://tools.ietf.org/html/rfc8484
#*******************************************************************************/

from log import setup_log,main_log
from log import logging
import subprocess
import sys
import time

# IMPORT MY STANDRT CLASS
from config import Config
from dropdns import DNS_DROP

#Import CLASS OF DNS UDP(INPUT)
if Config.I_UDPENABLE==True:
  from i_udp import Input_UDP

#Import CLASS OF DNS TCP(INPUT)
if Config.I_TCPENABLE==True:
  from i_tcp import Input_TCP

#Import CLASS OF DNS OVER TLS(INPUT)
if Config.I_DOTENABLE==True:
  from i_dot import Input_DOT

#Import CLASS OF DNS OVER HTTPS(INPUT)
if Config.I_DOHENABLE==True:
  from i_doh import Input_DOH

#Import CLASS OF DNS BY UDP(OUTPUT) 
if Config.O_UDPENABLE==True:
  from o_udp import OUTPUT_UDP

#Import CLASS OF DNS BY UDP(OUTPUT) 
if Config.O_TCPENABLE==True:
  from o_tcp import OUTPUT_TCP

#Import CLASS OF DNS BY DOH(OUTPUT) 
if Config.O_DOHENABLE==True:
  from o_doh import OUTPUT_DOH

#Import CLASS OF DNS BY DOT(OUTPUT) 
if Config.O_DOTENABLE==True:
  from o_dot import OUTPUT_DOT

# POINTER OF OUTPUT
output =None

# POINTER OF DROPDNS
dropdns =None


#/*******************************************************************************
# @author       Black-Blade
# @brief        test the ip of contry 
#               please install geoip-bin in systen
# @date         06.03.2021
# @param        [host(ip)]
# @return       [status(True,False),text]
# @version      0.0.1 Doxygen style eingebaut und erstellen dieser File
# @see          
# *******************************************************************************/
def geoip(host):
  logging.debug ("")

  # TEST IP IN GEOIP IN OS
  process = subprocess.run(['geoiplookup', host], capture_output=True)
  data = str(process.stdout)
  if data.find("IP Address not found") >= 0:
    return [True,str(host)]

  elif data.find("Germany") >= 0:
    return [True,"from Germany"]
  return [False,"Not from Germany"]

#/*******************************************************************************
# @author       Black-Blade
# @brief        all data coming her bevor go to select output 
# @date         06.03.2021
# @param        [txdata(dns request)]
# @return       [isblock,rxdata,blockname,dname]
# @version      0.0.1 Doxygen style eingebaut und erstellen dieser File
# @see          
# *******************************************************************************/

def switch(txdata):
  logging.debug ("")
  
  # NO OUTPUT SET RETURN NONE
  if output is None:
    return None

  # TEST DOMIN IN FILTER 
  if dropdns is None:
    return None
  
  isblock,rxblock,blockname,dname =dropdns.drop(txdata)
  if isblock==True:
    rxdata= rxblock
  else:
    rxdata = output.send(txdata)
  return  [isblock,rxdata,blockname,dname]

#/*******************************************************************************
# @author       Black-Blade
# @brief        mainprogramm start
# @date         06.03.2021
# @param        
# @return       
# @version      0.0.1 Doxygen style eingebaut und erstellen dieser File
# @see          
# *******************************************************************************/

if __name__ == "__main__":
  setup_log()
  main_log()

  if Config.O_UDPENABLE == True and \
     Config.O_TCPENABLE == True and \
     Config.O_DOHENABLE == True and \
     Config.O_DOTENABLE==True:
      logging.error("OS error: to many outputs set")
      quit()

  if Config.O_UDPENABLE == False and \
     Config.O_TCPENABLE == False and \
     Config.O_DOHENABLE == False and \
     Config.O_DOTENABLE==  False :
      logging.error("OS error: no outputs set")
      quit()

  if Config.I_UDPENABLE == False and \
     Config.I_TCPENABLE == False and \
     Config.I_DOTENABLE == False and \
     Config.I_DOHENABLE==  False :
      logging.error("OS error: no input set")
      quit()

  dropdns =DNS_DROP()
    
  #ENABLE CLASS OF DNS BY UDP(OUTPUT) 
  if Config.O_UDPENABLE==True:
    output= OUTPUT_UDP()
  
  #ENABLE CLASS OF DNS BY TCP(OUTPUT) 
  if Config.O_TCPENABLE==True:
    output= OUTPUT_TCP()

  #ENABLE CLASS OF DNS BY DOH(OUTPUT) 
  if Config.O_DOHENABLE==True:
    output= OUTPUT_DOH()

  #ENABLE CLASS OF DNS BY DOT(OUTPUT) 
  if Config.O_DOTENABLE==True:
    output= OUTPUT_DOT()

  #ENABLE CLASS OF DNS UDP (INPUT)
  if Config.I_UDPENABLE==True:
    i_udp=Input_UDP(switch,geoip)
    i_udp.init()

  #ENABLE CLASS OF DNS TCP (INPUT)
  if Config.I_TCPENABLE==True:
    i_tcp=Input_TCP(switch,geoip)
    i_tcp.init()

  #ENABLE CLASS OF DNS OVER TLS (INPUT)
  if Config.I_DOTENABLE==True:
    i_dot=Input_DOT(switch,geoip)
    i_dot.init()
  
#Import CLASS OF DNS OVER HTTPS(INPUT)
  if Config.I_DOHENABLE==True:
    i_doh=Input_DOH(switch,geoip)
    i_doh.init()

  while True:
    time.sleep(10)

#LOGS CLASS OF DNS UDP (INPUT)
    if Config.I_UDPENABLE==True:
      i_udp.logs()

#LOGS CLASS OF DNS TCP (INPUT)
    if Config.I_TCPENABLE==True:
      i_tcp.logs()

#LOGS CLASS OF DNS OVER TLS (INPUT)
    if Config.I_DOTENABLE==True:
      i_dot.logs()
    
#LOGS CLASS OF DNS OVER HTTPS(INPUT)
    if Config.I_DOHENABLE==True:
      i_doh.logs()

            

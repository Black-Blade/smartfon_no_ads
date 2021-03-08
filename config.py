#!/usr/bin/env python3
#/***************************************************************************//**
#	@file					config.py
#								
#	@author					Black-Blade 
#	@brief					config.py 
#	@date    				06.03.2021
#	@version				0.0.1 Doxygen style eingebaut und erstellen dieser File
#
#*******************************************************************************/

from log import logging

if __name__ == "__main__":
    quit()

class Config:
    # LOGLEVEL 

    #DEBUG
    #INFO
    #WARNING
    #ERROR
    #CRITICAL
    LOGLEVEL = logging.INFO
    LOGFILEENABLE = False
    LOGFILE  = "domains.log"

    # SSL CERTIFICATE
    CERTFILE ='/etc/certificate/xxx/fullchain.pem' 
    CERTPKEY ="/etc/certificate/xxx/privkey.pem"

    #DROP OF DNS REQUEST
    DROPPYHOLEENABLE = True
    DROPPYHOLEGRAVITYDB = '/etc/pihole/gravity.db'
    DROPLISTENABLE = True
    DROPLISTFILE ="list.txt"
    DROPTIMEDNSBUFFER = 2  

    # INPUTS OF DNS REQUEST
    I_UDPENABLE = True
    I_UDPSERVER ="0.0.0.0"
    I_UDPPORT = 4053
   
    I_TCPENABLE = True
    I_TCPSERVER ="0.0.0.0"
    I_TCPPORT = 4053
    I_TCPTIMEOUT = 0.5

    I_DOTENABLE = True
    I_DOTSERVER ="0.0.0.0"
    I_DOTPORT = 853
    I_DOTTIMEOUT = 0.5

    I_DOHENABLE = True
    I_DOHSERVER ="0.0.0.0"
    I_DOHPORT = 8853
    I_DOHPATH = "/dns"

    # OUTPUTS OF DNS REQUEST (SELECT ONLY ONE !!)
    O_UDPENABLE = True
    O_UDPSERVER ="172.20.0.2"
    O_UDPPORT = 53

    O_TCPENABLE = False
    O_TCPSERVER ="172.20.0.2"
    O_TCPPORT = 53
    O_TCPTIMEOUT = 0.5

    O_DOHENABLE = False
    #SEE IN o_doh.py 
    O_DOHSERVER ="ffmuc-post"
    
    O_DOTENABLE = False
    #SEE IN o_dot.py 
    O_DOTSERVER ="dismail1"
    O_DOTTIMEOUT=1

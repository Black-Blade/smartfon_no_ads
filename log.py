#!/usr/bin/env python3
#/***************************************************************************//**
#@file			log.py
#								
#@author		Black-Blade 
#@brief			log.py 
#@date    		13.1.2020
#@version	    0.0.1 Doxygen style eingebaut und erstellen dieser File
#
#***************************************************************************//**
import logging
import sys

# IMPORT MY STANDRT CLASS
from config import Config

if __name__ == "__main__":
    main_log()

#/*******************************************************************************
# @author       Black-Blade
# @brief        start the log of programm
# @date         06.03.2021
# @param        
# @return       
# @version      0.0.1 Doxygen style eingebaut und erstellen dieser File
# @see          
# *******************************************************************************/
def setup_log():
    if Config.LOGFILEENABLE==True:
        logging.basicConfig(format='%(asctime)18s %(levelname)8s %(module)8s:%(funcName)20s: %(message)s', datefmt='%d-%b-%y %H:%M:%S',level=Config.LOGLEVEL,filemode='a',filename=Config.LOGFILE)
    else:
        logging.basicConfig(format='%(asctime)18s %(levelname)8s %(module)8s:%(funcName)20s: %(message)s', datefmt='%d-%b-%y %H:%M:%S',level=Config.LOGLEVEL)

#/*******************************************************************************
# @author       Black-Blade
# @brief        log the prgramm info
# @date         06.03.2021
# @param        
# @return       
# @version      0.0.1 Doxygen style eingebaut und erstellen dieser File
# @see          
# *******************************************************************************/
def main_log():
    setup_log()
    logging.info("Start Programm")
    logging.info("Python version : "+sys.version.replace("\n",""))


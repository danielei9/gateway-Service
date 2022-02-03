#RPI.GPIO as GPIO
import os
import json
import glob
import psutil
import subprocess
import sys
from subprocess import PIPE
######################################################
print("Creando Proceso Lora")
command = "journalctl -u gesinen-sentilo-connector -f"
process = subprocess.Popen(
    command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell = True)
while(True):
#####################################################
#TX_ RX LORA
# #######################################################
    line = process.stdout.readline()
    if not line:
        print("not line")
        break
  #the real code does filtering here
    #print("LORA:", line.rstrip()
    if(line != ''):
        if ("### RECEIVED APPLICATION MESSAGE ###" in str(line)) :
            #Modules.Serial_me.SerialWrite(portConfig,"3_RX") #RX
            print("RX_LORA")
            sys.stdout.write(str(line))
            sys.stdout.flush()
        if(str(line).count("tx")):
            #Modules.Serial_me.SerialWrite(portConfig,"3_TX") #TX
            print("TX_LORA")


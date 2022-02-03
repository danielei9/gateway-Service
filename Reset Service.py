#RPI.GPIO as GPIO
import os
import json
import glob
import serial
#os.system("sudo reboot")
#os.system("sudo shutdown now")
import Modules.Serial_me
import Modules.MQTT as mqtt
baudrate  = 9600
import psutil
import subprocess
import sys
from subprocess import PIPE
######################################################
print("Creando Proceso Lora")
command = "journalctl -u gesinen-sentilo-connector -f"
process = subprocess.Popen(
    command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell = True)
######################################################
state = False

# mqtt

# SERIAL CONFIG#####################################################
portConfig = Modules.Serial_me.SerialBegin(baudrate) 
# Get cpuload #####################################################
def get_cpuload():
    cpuload = psutil.cpu_percent(interval=1, percpu=False)
    return str(cpuload)
#TEMP HUM#####################################################
while(True):
    if(Modules.Serial_me.SerialAvailable(portConfig)):
        data = str(Modules.Serial_me.SerialRead(portConfig))
        if(data.count("Temperature: ")):
            arr = data.split(' ')
            temp = arr[2].split('C')[0]
            print("temp" + temp)
        if(data.count("Humidity: ")):
            arr = data.split(' ') # arr[]
            hum = arr[4].split('%')[0]
            print("hum" + hum)
            mqtt.sendHumTempMQTT(hum,temp)
######################################################
######################################################
    try:
        d = str(subprocess.check_output("ping -c 4 google.es", shell=True))
        if(d.find ("4 received")):
            print("Internet connected")
            if(state == False):
                Modules.Serial_me.SerialWrite(portConfig,"1_1")
                state = True
                print("SEND")
        else:
            print("NO Internet connected")
            print(state)
            if(state == True):
                Modules.Serial_me.SerialWrite(portConfig,"1_0")
                state = False
    except:
        print("NO Internet connected")
        if(state == True):
                Modules.Serial_me.SerialWrite(portConfig,"1_0")
                state = False
        pass
#####################################################
#TX_ RX LORA
# #######################################################
    line = process.stdout.readline()
    if not line:
        print("not line")
        break
    #print("LORA:", line.rstrip()
    if(line != ''):
        if ("### RECEIVED APPLICATION MESSAGE ###" in str(line)) : #SI QUE VA 
            #Modules.Serial_me.SerialWrite(portConfig,"3_RX") #RX
            print("RX_LORA")
            sys.stdout.write(str(line))
            sys.stdout.flush()
        if(str(line).count("tx")): ### NO SE ENVIA POR JOURNAL NO VA TX  PERO CADA VEZ QUE RECIBE SI QUE VA 
            #Modules.Serial_me.SerialWrite(portConfig,"3_TX") #TX
            print("TX_LORA")
#####################################################
#CPU
    print(get_cpuload())
    if(float(get_cpuload()) > 1 ):
        Modules.Serial_me.SerialWrite(portConfig,"4_CPU")
#####################################################

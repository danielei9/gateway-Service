import subprocess
import sys
from subprocess import PIPE
command = "journalctl -u gesinen-sentilo-connector -f"
process = subprocess.Popen(
command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell = True)
while True:
    line = process.stdout.readline()
    if not line:
        break
  #the real code does filtering here
    print("test:", line.rstrip())
  
    if(line != ''):
        sys.stdout.write(str(line))
        sys.stdout.flush()
        if(str(line).count("rx")):
            print("RX_LORA")
        if(str(line).count("tx")):
            print("TX_LORA")

import serial
import glob

def serial_ports():
    ports = glob.glob('/dev/tty[A-Za-z]*')
    print("buscando puertos")
    result = []
    for port in ports:
        try:
            print(port)
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    print(result[0])
    return result
def SerialBegin(baud):
    try:
        print("Connecting to Arduino NANO")
        portConfig   = serial.Serial(port = serial_ports()[0],
                         baudrate = baud,
                         bytesize = serial.EIGHTBITS,
                         parity   = serial.PARITY_NONE,
                         stopbits = serial.STOPBITS_ONE)
    except:
        SerialBegin(baud)
        print("Reconnecting to Arduino NANO")
        time.sleep(5)
        pass
    return portConfig
def SerialWrite(portConfig,xData):
    try:
        portConfig.write(str(xData).encode())
    except:
        portConfig.close()
        time.sleep(2)
        SerialBegin(9600)
        

def SerialClose(portConfig):
    portConfig.close()

def SerialOpen(portConfig):
    portConfig.open()

def SerialRead(portConfig):
   return portConfig.readline()

def SerialAvailable(portConfig):
    if(portConfig.in_waiting):
        return True
    else:
        return False
#SerialBegin(9600)

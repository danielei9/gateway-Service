import paho.mqtt.client as paho
import random
import time
import json
import os

topic_general = ""
def updateConfigMqtt(data,clt): 
    print("updating config MQTT")
    if(not os.path.exists('configMQTT.json')):
        with open('configMQTT.json', 'w') as file:
            json.dump(data, file, indent=4)
            print("file:")
            print(file)
    if(clt != None):
        try:
            print("clt reinitialise")
            clt.disconnect() # disconnect gracefully
            clt.loop_stop() # stops network loop
            time.sleep(2)
            data = data.split("\"")
#           GET DATA
            broker = data[4][:-1] 
            topic = data[8][:-1]
            client = data[12][:-1]
            pswd = data[16][:-1]
            user = data[20][:-1]
            #Reiniciar cliente
            clt.reinitialise(client_id=client, clean_session=True, userdata=None)
#           activar TLS
            clt.tls_set()
            print("usr:" + str(username) + "  pswd:" + str(pswd) +"  broker:" + str(broker) +"  port:" + str(port)+ "  topic:" + str(topic))
#           Loop de escucha MQTT
            createLoopMqttRecive(clt,username,pswd,broker,port,topic)
            time.sleep(2)
#           Publicar TODO OK
            clt.publish(topic +"/rx","{\"status\":\"OK Connected to "+str(topic)+"\"}") # DEVUELVE OK A TOPIC/rx PORCIERTO EL TOPICO DEBE CAMBIAR 
        except Exception as inst:
#           Si hay una excepcion publica error e intenta actualizar la información
            print(inst)
            clt.publish(topic +"/rx","{\"status\":\"EXCEPT initMqtt trying again..."+str(topic)+"\"}") # DEVUELVE NO OK A TOPIC/rx PORCIERTO EL TOPICO DEBE CAMBIAR 
            print("EXCEPT initMqtt")
            updateConfigMqtt(data,clt)
            time.sleep(5)
            pass
#Cuando llega un mensaje
def on_message(clt, usrdata, mess):
    time.sleep(1);
    incomingStr = str(mess.payload.decode("utf-8"))
    print(incomingStr)
    configMqtt = json.dumps(incomingStr)
    updateConfigMqtt(configMqtt,clt)

def sendHumTempMQTT(hum,temp):
    dataJson = {
      "Temp": temp,
      "Hum": hum
    }
    try:
        with open('configMQTT.json', 'r') as file:
            configMqtt = json.load(file)
            configMqtt = json.loads(configMqtt)
            topic = configMqtt["topic"]
            print("GETTING TOPIC TO SEND HUM TEMP TO:" + topic)
        clt.publish(topic +"/data",json.dumps(dataJson))
    except:
        clt.publish(topic_general +"/rx","{\"status\":\"ERROR SENDING.."+str(topic)+"\"}") # DEVUELVE NO OK A TOPIC/rx PORCIERTO EL TOPICO DEBE CAMBIAR
        pass

def createLoopMqttRecive(clt,username,password,broker,port,topic):
    #Damos callback a usar cuando hay un msg
    clt.on_message = on_message
    print("conectando al broker", broker)
    try:
        print("setting username: " +username + "  pass: " + password)
        clt.username_pw_set(username=username, password=password)
        print(clt.connect(broker,int(port)))
    except:
        print("connection failed")
        print("Try to reconnect")
        time.sleep(2)
        createLoopMqttRecive(clt,username,password,broker,port,topic)

       # exit(1) #Should quit or raise flag to quit or retry
    try:
        clt.loop_start() # Inicia el bucle esperando a un msg
        print("subscribiendo... " +topic+"/config" )
        topic_general = topic

        if(os.path.exists('configMQTT.json')):
            modelXconfig = {
                "broker": str(broker),
                "topic": str(topic),
                "client": "Client-Gateway"+ str(random.randint(0, 10000000)),
                "password": str(password),
                "username": str(username),
                "port":int(port)
             }
            data = json.dumps(modelXconfig)
            with open('configMQTT.json', 'w') as file:
                json.dump(data, file, indent=4)
                print("data:")
                print(data)
        clt.subscribe(topic+"/config")
        topic_general = topic
#         print("prueba de publicación:")
#         msg = "LOW"
#         clt.publish(topic+"/data",msg)
    except:
        print("subscribe Failed")
        
def initMQTT():   
    try:
        print("initMQTT")
        print("Open configMQTT.json")
        with open('configMQTT.json', 'r') as file:
            configMqtt = json.load(file)
            print("LAST:"+configMqtt)
            return configMqtt
    except Exception as inst:  #  revisar FALLA LECTURA LA 2º VEZ DE LOS DATOS 
        print(inst)
        print("EXCEPT initMqtt")
#         modelXconfig = {
#             "broker": "gesinen.es",
#             "topic": "gateway/cambiartopic",
#             "client": "Client-Gateway"+ str(random.randint(0, 10000000)),
#             "password": "gesinen2110",
#             "username": "gesinen",
#             "port":8882
#         }
#         configInitialMqtt = json.dumps(modelXconfig)
#         updateConfigMqtt(configInitialMqtt,None)
        return  configMqtt

configMQTT = json.loads(initMQTT())
print(configMQTT)

broker = configMQTT["broker"]
topic = configMQTT["topic"]
topic_general = topic
client = configMQTT["client"]
username = configMQTT["username"]
password = configMQTT["password"]
port = configMQTT["port"]
clt=paho.Client(client,True)
clt.tls_set()
print(configMQTT)
createLoopMqttRecive(clt,configMQTT["username"],configMQTT["password"],configMQTT["broker"],configMQTT["port"],configMQTT["topic"])
sendHumTempMQTT(str("TEST"),str("TEST"))
# while(True):
#     d=1
 
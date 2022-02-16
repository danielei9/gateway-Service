# gateway-Service

ESTE SERVICIO ES PARA CONTROLAR EL HARDWARE AÑADIDO AL GATEWAY LA PLACA RESET SECURE CONTIENE UN ARDUINO Y U SENSOR HUMEDAD Y TEMPERATURA  Y OPCIONALMENTE SE PUEDE CONFIGURAR EL HARDWARE PARA INICIALIZAR EL UPS CON CADA INICIO

// Dependencies 
Actualización
sudo apt-get upgrade
sudo apt-get update

Instalacion de pip: Sabremos si esta instalado mediante el comando en terminal de:
sudo apt install python3-pip -y
pip3 --version

pip3 install pyserial
pip3 install paho-mqtt python-etcd
pip3 install psutil

probar si todo va bien 
cd gateway-Service 
./init-python.sh

/***************************************************************************************/
PARAMETROS DE INSTALACION DEL SERVICIO
/***************************************************************************************/
 1. Hacer git clone de este repositorio en /home/pi/
 2. Entrar en crontab -e  mediante una terminal, y escribir dentro del archivo (sin comillas):  "@reboot  /home/pi/gateway-Service/init-python.sh > /tmp/HUMTEMP_LEDS_SWITCH.log 2>&1"
 3. dar permisos de ejecucion mediante terminal con:  chmod +x /home/pi/gateway-Service/init-python.sh 
 4. podemos ver el log al reinicar   --> nano /tmp/HUMTEMP_LEDS_SWITCH.log
/home/pi/gateway-Service/init-python.sh  -->  python3 /home/pi/gateway-Service/Reset\ Service.py


Cambiar topico gateway-service:

	API MQTT 
		Al iniciar el servicio la primera vez se ejecuta con este topico  "gateway/cambiartopic2/config" el cual se debe de cambiar mediante un 
		publicación mqtt, la cual configura el servidor del mqtt y el topico: NO PONER EL MISMO TOPICO QUE ANTERIORMENTE SI NO HAY QUE REINICIAR EL SERVICIO PENDIENTE DE ACTUALIZACION
```javascript		
ENVIAR A  TOPICO : gateway/cambiartopic12/config (comprobar en archivo de config  configMQTT.json)
{
	"broker":"gesinen.es",
	"topic":"b827eb9fd77c/application/2/gatewayService",
	"client":"b827eb9fd77c",
	"password":"gesinen2110",
	"username":"gesinen",
	"port":8882
}
```
Recibir datos 
SUBSCRIBE TO topic + /data 
	ejemplo : gateway/cambiartopic/data




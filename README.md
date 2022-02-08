# gateway-Service

ESTE SERVICIO ES PARA CONTROLAR EL HARDWARE AÑADIDO AL GATEWAY LA PLACA RESET SECURE CONTIENE UN ARDUINO Y U SENSOR HUMEDAD Y TEMPERATURA  Y OPCIONALMENTE SE PUEDE CONFIGURAR EL HARDWARE PARA INICIALIZAR EL UPS CON CADA INICIO

Cambiar topico gateway-service:

	API MQTT 
		Al iniciar el servicio la primera vez se ejecuta con este topico  "gateway/cambiartopic2/config" el cual se debe de cambiar mediante un 
		publicación mqtt, la cual configura el servidor del mqtt y el topico: NO PONER EL MISMO TOPICO QUE ANTERIORMENTE SI NO HAY QUE REINICIAR EL SERVICIO PENDIENTE DE ACTUALIZACION
```javascript		
ENVIAR A  TOPICO : gateway/cambiartopic2/config
{
	"broker":"gesinen.es",
	"topic":"gateway/cambiartopic",
	"client":"CLTGAT",
	"password":"gesinen2110",
	"username":"gesinen",
	"port":8882
}
```
Recibir datos 
SUBSCRIBE TO topic + /data 
	ejemplo : gateway/cambiartopic/data


/***************************************************************************************/
PARAMETROS DE INSTALACION DEL SERVICIO
/***************************************************************************************/
crontab -e  --> @reboot  /home/pi/gateway-Service/init-python.sh > /tmp/HUMTEMP_LEDS_SWITCH.log 2>&1

LOG EN   --> /tmp/HUMTEMP_LEDS_SWITCH.log

dar permisos de ejecucion chmod +x /home/pi/gateway-Service/init-python.sh 

/home/pi/gateway-Service/init-python.sh  -->  python3 /home/pi/gateway-Service/Reset\ Service.py

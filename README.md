# mqtt

MQTT Publisher/Subscriber

Este proyecto es una implementación de publicador y suscriptor MQTT utilizando Python.

Características
Publicador MQTT: Envía mensajes a un tema específico.
Suscriptor MQTT: Recibe e imprime mensajes de un tema específico.
Requisitos previos
Para ejecutar este proyecto, necesitas tener los siguientes requisitos previos:

Python 3.x instalado
Biblioteca Paho MQTT instalada (se puede instalar con pip install paho-mqtt)
Instalación
Clona el repositorio:
bash
Copy code
git clone https://github.com/jamart25/mqtt.git
Ingresa al directorio del proyecto:
bash
Copy code
cd mqtt
Uso
Publicador
Para publicar un mensaje en un tema, ejecuta el script publisher.py con los parámetros deseados:

bash
Copy code
python publisher.py --broker <direccion_broker> --port <puerto_broker> --topic <tema> --message <mensaje>
Reemplaza <direccion_broker> con la dirección del broker MQTT, <puerto_broker> con el número de puerto, <tema> con el tema deseado y <mensaje> con el mensaje a publicar.

Suscriptor
Para suscribirte a un tema y recibir mensajes, ejecuta el script subscriber.py con los parámetros deseados:

bash
Copy code
python subscriber.py --broker <direccion_broker> --port <puerto_broker> --topic <tema>
Reemplaza <direccion_broker> con la dirección del broker MQTT, <puerto_broker> con el número de puerto y <tema> con el tema al que deseas suscribirte.

import paho.mqtt.client as mqtt
import time


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(username="scs",password="scs")
client._connect_timeout = 1.0


while True:
	try:
		client.connect("localhost", 1883, 60)
		print("connetti")
	except:
		print("ERRORE CONNESSSIONE")
		time.sleep(1)
	else:
		print("CONNESSOOOOOOOOOOOOOOOOOO")
		client.disconnect()
		break




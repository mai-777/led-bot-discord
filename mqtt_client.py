import paho.mqtt.client as mqtt

class MQTTClient:
    def __init__(self, broker, port):
        self.broker = broker
        self.port = port
        self.client = mqtt.Client()
        
    def connect(self):
        try:
            self.client.connect(self.broker, self.port)
            self.client.loop_start()
            print("Conectado al broker MQTT")
            return True
        except Exception as e:
            print(f"Error al conectar al broker MQTT: {e}")
            return False
    
    def publish(self, topic, message):
        self.client.publish(topic, message)
        print(f"Mensaje publicado: {message} en {topic}")
    
    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
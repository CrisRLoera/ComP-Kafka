from kafka import KafkaConsumer
import json

class Consumer:
    def __init__(self):
        self.consumer = KafkaConsumer(
            'NASA', 
            bootstrap_servers='localhost:9092',
            auto_offset_reset='earliest', 
            enable_auto_commit=True,
            group_id='nasa-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))  
        )
        print("Consumidor inicializado y escuchando al topic 'NASA'...")

    def start_consume(self):
        try:
            for message in self.consumer:
                print(f"Mensaje recibido: {message.value}")
                self.process_data(message.value)
        except KeyboardInterrupt:
            print("Consumo detenido manualmente.")

    def process_data(self, data):
        print("Procesando datos del topic 'NASA':")
        for key, value in data.items():
            print(f"{key}: {value}")


if __name__ == '__main__':
    consumer = Consumer()
    consumer.start_consume()

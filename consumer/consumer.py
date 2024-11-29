from kafka import KafkaConsumer
import json
from pymongo import MongoClient
import time
from flask import Flask, render_template
from flask_socketio import SocketIO
import threading

class Consumer:
    def __init__(self, socket_emit_callback):
        self.client = MongoClient('mongodb://Test:test@localhost:27017/')
        self.db = self.client['asteroid_alerts']
        self.collection = self.db['observations']

        self.consumer_weather = KafkaConsumer(
            'weatherData', 
            bootstrap_servers='localhost:9092',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))  
        )
        print("Consumidor inicializado y escuchando al topic 'weatherData'...")

        self.consumer_asteroids = KafkaConsumer(
            'asteroidsData', 
            bootstrap_servers='localhost:9092',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))  
        )
        print("Consumidor inicializado y escuchando al topic 'asteroidsData'...")

        self.socket_emit_callback = socket_emit_callback  # Callback para emitir datos al socket

    def start_consume(self):
        try:
            for asteroid in self.consumer_asteroids:
                for weather in self.consumer_weather:
                    # Emitir los datos al WebSocket
                    print("Sending")
                    observation = {
                        'asteroid_name': asteroid.value['name'],
                        'distance_km': asteroid.value['distance_km'],
                        'climate': weather.value['weather'],
                        'timestamp': int(time.time()),  # Timestamp en segundos
                        'observation_possible': weather.value['weather'] == 'clear sky',
                        'id': str(asteroid.value['_id']) if '_id' in asteroid.value else None  # Convertir ObjectId a string
                    }
                    self.socket_emit_callback('new_data', observation)
                    # Insertar en MongoDB
                    self.collection.insert_one(observation)
                    # Asegurarse de que todos los valores sean serializables
                    
        except KeyboardInterrupt:
            print("Consumo detenido manualmente.")

    def process_data(self, data):
        print("Procesando datos del topic 'NASA':")
        for key, value in data.items():
            print(f"{key}: {value}")

# Flask y SocketIO Setup
app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')  # Una plantilla básica de HTML

def consume_data():
    # Crear el consumidor con un callback para emitir datos a través de WebSocket
    consumer = Consumer(socket_emit_callback=socketio.emit)
    consumer.start_consume()

if __name__ == '__main__':
    # Iniciar el consumidor en un hilo separado para que no bloquee el servidor Flask
    threading.Thread(target=consume_data, daemon=True).start()
    
    # Ejecutar la aplicación Flask
    socketio.run(app, host='0.0.0.0', port=5000)

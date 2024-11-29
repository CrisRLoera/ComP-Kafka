# producer.py
from kafka import KafkaProducer
import time
import json
import pandas as pd
import requests
import sys


class Producer:
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092')
        self.data = None
        self.data2 = None
        self.CITY = 'Chihuahua'
        self.getNASAdata()


    def getNASAdata(self):
        WEATHER_API_KEY = '49109c93dfa31563d2787cbd0a47da5b'
        URL = f'https://api.openweathermap.org/data/2.5/weather?q={self.CITY}&appid={WEATHER_API_KEY}'

        response = requests.get(URL)
        #data = response.json()
        #response = requests.get('https://api.nasa.gov/insight_weather/?api_key=PwadD33p0Lv4czeAgWhDhzza6zxr2loCNzl9QBsU&feedtype=json&ver=1.0')
        response2 = requests.get('https://api.nasa.gov/neo/rest/v1/feed?api_key=PwadD33p0Lv4czeAgWhDhzza6zxr2loCNzl9QBsU')
        if response.status_code == 200:
            self.data = response.json()
            print("Datos obtenidos de Clima:",self.data)
        else:
            print(f"Error al obtener datos: {response.status_code}")

        if response2.status_code == 200:
            self.data2 = response2.json()
            print("Datos obtenidos de NASA:",self.data2)
        else:
            print(f"Error al obtener datos: {response2.status_code}")

    def start_write(self):
        while True:  # Bucle infinito para mantener las peticiones
            if self.data:
                future = self.producer.send('weatherData', json.dumps({
                    'city': self.CITY,
                    'weather': self.data['weather'][0]['description'],
                    'temperature': self.data['main']['temp'],
                    'date': self.data['dt']
                }).encode('utf-8'))
                result = future.get(timeout=10)
                print("Clima: Datos enviados a Kafka:", result)
            else:
                print("Clima: No hay datos para enviar a Kafka.")
            
            if self.data2:
                for date, asteroids in self.data2['near_earth_objects'].items():
                    for asteroid in asteroids:
                        future = self.producer.send('asteroidsData', json.dumps({
                            'name': asteroid['name'],
                            'size_km': asteroid['estimated_diameter']['kilometers']['estimated_diameter_max'],
                            'speed_kmh': asteroid['close_approach_data'][0]['relative_velocity']['kilometers_per_hour'],
                            'distance_km': asteroid['close_approach_data'][0]['miss_distance']['kilometers'],
                            'date': date
                        }).encode('utf-8'))
                        result = future.get(timeout=10)
                        print("NASA: Datos enviados a Kafka:", result)
            else:
                print("NASA: No hay datos para enviar a Kafka.")
            
            time.sleep(60)  # Espera 60 segundos antes de la siguiente petición

if __name__ == '__main__':
    producer = Producer()
    producer.start_write()
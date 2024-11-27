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
        self.getNASAdata()


    def getNASAdata(self):
        response = requests.get('https://api.nasa.gov/insight_weather/?api_key=PwadD33p0Lv4czeAgWhDhzza6zxr2loCNzl9QBsU&feedtype=json&ver=1.0')
        if response.status_code == 200:
            self.data = response.json()
            print("Datos obtenidos de NASA:", self.data)
        else:
            print(f"Error al obtener datos: {response.status_code}")

    def start_write(self):
        if self.data:
            future = self.producer.send('NASA', value=json.dumps(self.data).encode('utf-8'))
            result = future.get(timeout=10)
            print("Datos enviados a Kafka:", result)
        else:
            print("No hay datos para enviar a Kafka.")

if __name__ == '__main__':
    producer = Producer()
    producer.start_write()
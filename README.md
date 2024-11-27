# Data-pipeline Kafka Project

## Prerrequisitos

Se requiere tener instalado Docker y docker-compose para poder iniciar este proyecto

## Requerimientos

Una vez clonado este proyecto, y dentro de la ruta de este proyecto, se ejecuta el siguiente comando para crear y iniciar los contenedores de Docker.

```bash
    docker-compose up -d
```

## Crear topicos

Una vez creados los contenedores vamos a crear los topicos entrando a el contenedor de kafka

```bash
docker exec -it kafka bash
```
Y mediante el siguiente comando creamos un topic básico en kafka
```
kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic "NASA"

```

## Productor

Para pruducir un log en kafka solamente se debe de ejecutar el script de python
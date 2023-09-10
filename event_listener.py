from kafka import KafkaProducer, KafkaConsumer
from config import settings
import json

# Create an instance of the Kafka producer
producer = KafkaProducer(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

consumer = KafkaConsumer([settings.KAFKA_NER_TOPIC, settings.KAFKA_KEYWORDS_TOPIC],
                         bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS, value_deserializer=lambda m: json.loads(m.decode('utf-8')), 
                         auto_offset_reset='earliest', )

while True:
    messages = consumer.poll()
    for topic, messages in messages.items():
        if topic == settings.KAFKA_NER_TOPIC:
            for msg in messages:
                print(msg)
        elif topic == settings.KAFKA_KEYWORDS_TOPIC:
            for msg in messages:
                print(msg)

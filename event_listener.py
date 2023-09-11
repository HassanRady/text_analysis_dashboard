from kafka import KafkaConsumer
from config import settings
import json

from redis_handler import RedisClient
rc = RedisClient()

consumer = KafkaConsumer(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVER, value_deserializer=lambda m: json.loads(m.decode('utf-8')), 
                         auto_offset_reset='latest', )
consumer.subscribe([settings.KAFKA_NER_TOPIC, settings.KAFKA_KEYWORDS_TOPIC])

async def consume():
    while True:
        messages = consumer.poll()
        for topic, messages in messages.items():
            if topic.topic == settings.KAFKA_NER_TOPIC:
                for msg in messages:
                    rc.write_to_table(settings.KAFKA_NER_TOPIC, msg.timestamp, msg.value)
            elif topic.topic == settings.KAFKA_KEYWORDS_TOPIC:
                for msg in messages:
                    rc.write_to_table(settings.KAFKA_KEYWORDS_TOPIC, msg.timestamp, msg.value)

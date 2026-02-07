from kafka import KafkaProducer
import json

_producer = None


def get_producer():
    """
    Creates a Kafka producer only once (singleton).
    Reuses the same connection for all messages.
    """
    global _producer

    if _producer is None:
        try:
            _producer = KafkaProducer(
                bootstrap_servers="localhost:9092",
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                retries=3,
                acks="all"
            )
            print("✅ Kafka producer connected")
        except Exception as e:
            print("❌ Kafka not available:", e)
            _producer = None

    return _producer


def send_to_kafka(data, topic="trading-signals"):
    """
    Sends extracted trading data to Kafka topic.
    Fails gracefully if Kafka is down.
    """
    producer = get_producer()

    if producer:
        try:
            producer.send(topic, data)
            producer.flush()
            print("📤 Sent to Kafka:", data)
        except Exception as e:
            print("❌ Failed to send message to Kafka:", e)
    else:
        print("⚠️ Skipping Kafka send (producer not available)")
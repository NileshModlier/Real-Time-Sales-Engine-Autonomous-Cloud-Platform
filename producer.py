
import json, time, random, uuid, yaml
from datetime import datetime
from kafka import KafkaProducer

def load_config():
    with open('config/producer_config.yaml','r') as f:
        return yaml.safe_load(f)

def generate_event():
    return {
        "transaction_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "product_id": f"P{random.randint(100,999)}",
        "product_name": random.choice(["Mouse","Keyboard","Laptop","Monitor"]),
        "quantity": random.randint(1,5),
        "price_per_unit": random.choice([299,499,999,1999]),
        "store_location": random.choice(["Bangalore","Mumbai","Delhi"]),
        "payment_mode": random.choice(["UPI","Card","Cash"])
    }

def main():
    cfg = load_config()["kafka"]
    producer = KafkaProducer(
        bootstrap_servers=cfg["bootstrap_servers"],
        acks=cfg["acks"],
        linger_ms=cfg["linger_ms"],
        retries=cfg["retries"],
        request_timeout_ms=cfg["request_timeout_ms"],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    print("✅ Kafka Producer started...")
    while True:
        event = generate_event()
        producer.send(cfg["topic"], event)
        print("➡ Sent event:", event)
        time.sleep(1)

if __name__ == '__main__':
    main()

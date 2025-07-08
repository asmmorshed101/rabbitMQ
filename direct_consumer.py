import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

# CLI থেকে severity গুলো নিই
severities = sys.argv[1:] if len(sys.argv) > 1 else ['info']

for severity in severities:
    channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key=severity)

print(f"🟢 Waiting for messages for severities: {severities}")

def callback(ch, method, properties, body):
    print(f"📥 [{method.routing_key}] {body.decode()}")

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()

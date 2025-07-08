import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

# CLI থেকে severity (routing key) আর message নিতে চাই
severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
message = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else 'Hello Direct Exchange!'

channel.basic_publish(
    exchange='direct_logs',
    routing_key=severity,
    body=message
)

print(f"✅ Sent '{message}' with severity '{severity}'")
connection.close()

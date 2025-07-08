import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

# message = 'Hello to all queues!'
message = ' '.join(sys.argv[1:])
channel.basic_publish(exchange='logs', routing_key='', body=message)

print(f"✅ Sent: '{message}'")
connection.close()

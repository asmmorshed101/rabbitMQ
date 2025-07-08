import pika # Python libray for RabbitMQ, we can communicate with RabbitMQ with this library
import sys  # Take input from terminal

# Creating conection with RabbitMQ server which is running in localhost. BlockingConnection --> sysnc connection - it will wait until finishing the message.
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

# From the connection creating a channel. All the task is done through this channel like making queue, sending message.
channel = connection.channel()

# Creating a channel name direct_logs and declared type direct. It means using routing key it will go to a specific queue.
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

# Here it has been declared a random queue because name '' and exclusive = Ture means this queue will contain till the connection, if the connection close then queue will disappear. 
result = channel.queue_declare('', exclusive=True)

# Here it is contianing the queue name
queue_name = result.method.queue

# Taking input from command line. If not given then default is info
# Like python direct_consumer.py warning error
# Here severities = ['warning', 'error']

severities = sys.argv[1:] if len(sys.argv) > 1 else ['info']

# Sending message to the specific queue after getting the key from severities. 
for severity in severities:
    channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key=severity)

print(f"🟢 Waiting for messages for severities: {severities}")

# After getting the message what if will print the routing key and message 
def callback(ch, method, properties, body):
    print(f"📥 [{method.routing_key}] {body.decode()}")

# Take message from queue, process it through callback, auto_ack=True means consumer will acknowledge RabbitMQ after getting a message. 

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

# It will start listening message untill you press Ctrl+C
channel.start_consuming()

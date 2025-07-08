import pika # Python libray for RabbitMQ, we can communicate with RabbitMQ with this library
import sys  # Take input from terminal

# Creating conection with RabbitMQ server which is running in localhost. BlockingConnection --> sysnc connection - it will wait until finishing the message. 
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

# From the connection creating a channel. All the task is done through this channel like making queue, sending message.
channel = connection.channel()

# Creating a channel name direct_logs and declared type direct. It means using routing key it will go to a specific queue.
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

# It will take routing key from command line like info, warning, error. If not given then it will ifo by default
severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
# It will take message part if not given then default "Hello Direct Exchange!"
message = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else 'Hello Direct Exchange!'

# Example if you write python direct_producer.py error "Database connection failed"
# Then serverity = 'error' and message = 'Database connection failed'

# Here declareing message where it will go
channel.basic_publish(
    exchange='direct_logs',
    routing_key=severity,
    body=message
)

# We can understand which routing key and what message has been sent
print(f"✅ Sent '{message}' with severity '{severity}'")
connection.close()

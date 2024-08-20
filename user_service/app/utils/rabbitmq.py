import pika
import os

def send_message_to_rabbitmq(email):
    rabbitmq_host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
    rabbitmq_port = int(os.getenv('RABBITMQ_PORT', 5672))
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port))
    channel = connection.channel()
    channel.queue_declare(queue='email_queue')
    channel.basic_publish(exchange='',
                          routing_key='email_queue',
                          body=email)
    connection.close()

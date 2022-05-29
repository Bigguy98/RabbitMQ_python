import pika
import sys
import os

def main():
    # create connection
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)

    while True:
        message = raw_input('Type your message with number of dots: ')
        channel.basic_publish(exchange='',
            routing_key='task_queue',
            body=message,
            properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)) # this option make sure message will be store at rabbitMQ event if it down or restart
        print('[x] sent %r' % message)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
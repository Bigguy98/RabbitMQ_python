import pika
import time
import sys
import os


def getCurrentTime():
    return time.strftime("%H:%M:%S", time.localtime())


def callback(ch, method, properties, body):
    print( getCurrentTime() + ' [x] Received message:  %r' % body.decode())
    time.sleep(body.count(b'.'))
    print(getCurrentTime() + ' [x] job done')
    # manual ack
    ch.basic_ack(delivery_tag=method.delivery_tag) 

def main():
    # create connection
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    # tell RabbitMQ not send message to worker until it ack the previous message
    channel.basic_qos(prefetch_count=1)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.basic_consume(queue='task_queue', on_message_callback=callback)
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
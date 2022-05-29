import pika
import sys, os


def callback(ch, method, properties, body):
    print('[x] recveived %r:%r' % (method.routing_key,body))


def main():
    # create connection
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    # declare exchange
    channel.exchange_declare(exchange='topic_logs', exchange_type='topic')
    # create a random name, auto delete when close queue 
    queue = channel.queue_declare(queue='', exclusive=True)
    # binding exchange, so exchange know which queue to push message to
    supported_routing_keys = ['kern.info.*', '*.blue.chip', 'green.#']
    for rk in supported_routing_keys:
        channel.queue_bind(exchange='topic_logs',queue=queue.method.queue, routing_key=rk)
    print(' [*] Waiting for logs. To exit press CTRL+C')
    channel.basic_consume(queue=queue.method.queue, on_message_callback=callback, auto_ack=True)
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
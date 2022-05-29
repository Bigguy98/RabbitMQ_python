import pika
import sys, os


def main():
    # create connection
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    # declare exchange
    channel.exchange_declare(exchange='logs', exchange_type='fanout')
    print('Press Ctrl + C to close the terminal.')
    while True:
        message = raw_input('Type your message:')
        # send the message to exchange
        channel.basic_publish(exchange='logs',
            routing_key='',  # normally this will be the queue name
            body=message)
        print("[x] Sent the message %r" % message)
    connection.close()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
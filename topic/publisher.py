import pika
import sys, os


def main():
    # create connection
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    # declare exchange
    channel.exchange_declare(exchange='topic_logs', exchange_type='topic')
    print('Press Ctrl + C to close the terminal.')
    while True:
        routing_key = raw_input('routing_key:') # should in format: abc.txt.*
        message = raw_input('Type your message:')
        # send the message to exchange
        channel.basic_publish(exchange='topic_logs',
            routing_key=routing_key,  
            body=message)
        print("[x] Sent the message %r with routing_key %r" % (message, routing_key))
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
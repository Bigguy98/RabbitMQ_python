import pika
import sys, os


def main():
    # create connection
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    # declare exchange type direct for routing message by serverity
    channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
    print('Press Ctrl + C to close the terminal.')
    serverities = ['error', 'warning', 'info']
    while True:
        serverity = raw_input('Serverity:')
        if serverity not in serverities:
            print("Not suitable serverity!")
            continue
        message = raw_input('Type your message:')
        # send the message to exchange
        channel.basic_publish(exchange='direct_logs',
            routing_key=serverity,  # normally this will be the queue name, here we use serverity as filter for routing
            body=message)
        print("[x] Sent the message %r with type %r" % (message, serverity))
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
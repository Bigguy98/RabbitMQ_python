import pika

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    # create message queue
    channel.queue_declare(queue='greeting')
    print(' [*] Type the messages and press Enter. To exit press CTRL+C')
    while True:
        message = raw_input("Message: ")
        channel.basic_publish(exchange='',
                    routing_key='greeting',
                    body=message)
        print('[x] sent message: '  + message)

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
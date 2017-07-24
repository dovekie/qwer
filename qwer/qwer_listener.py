import pika
import requests
from qwer import write_data_to_db

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='jobs')

def callback(ch, method, properties, body):
    params = body.split()
    print 'Got a job to do with {}'.format(params[1])
    r = requests.get(url=params[1])
    print r.status_code
    write_data_to_db(params[0], r.text)

channel.basic_consume(callback,
                      queue='jobs',
                      no_ack=True)

print('Rabbit is waiting for messages. To exit press CTRL+C')
channel.start_consuming()
import pika
import requests
from qwer import qwer
from model import Job, connect_to_db
from model import db as alchemy_db

connect_to_db(qwer)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='jobs')

def callback(ch, method, properties, body):
    params = body.split()
    r = requests.get(url=params[1])
    job = Job.query.filter_by(id=params[0]).first()
    job.data = r.text
    alchemy_db.session.commit()

channel.basic_consume(callback,
                      queue='jobs',
                      no_ack=True)

print('Rabbit is waiting for messages. To exit press CTRL+C')
channel.start_consuming()
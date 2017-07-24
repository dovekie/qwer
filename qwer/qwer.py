import os
import sqlite3
import json
import pika
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from model import Job, connect_to_db
from model import db as alchemy_db

qwer = Flask(__name__)

qwer.config.from_object(__name__)

qwer.config.update(dict(
	DATABASE=os.path.join(qwer.root_path, 'qwer.db'),
	SECRET_KEY='development key',
	USERNAME='admin',
	PASSWORD='default'
))

qwer.config.from_envvar('QWER_SETTINGS', silent=True)

#########
# VIEWS #
#########

@qwer.route('/')
def index():
	resp = {'data': {},
			'links': {'self': 'http://127.0.0.1:5000/',
					  'start a job': 'http://127.0.0.1:5000/job',
					  'check job status': 'http://127.0.0.1:5000/job?id=[id]'
					  }
			}
	return json.dumps(resp)

@qwer.route('/job/', methods=['GET', 'POST'])
@qwer.route('/job/<jobId>', methods=['GET'])
@qwer.route('/job/<jobId>', methods=['DELETE'])
def show_jobs(jobId=None):
	""" Get jobs from the queue """
	if request.method == 'POST':
		""" Add a job to the queue """
		new_job = Job(status='new', location=request.form['location'])
		alchemy_db.session.add(new_job)
		alchemy_db.session.commit()
		return redirect(url_for('show_jobs'))
	if jobId:
		if request.method == 'GET':
			entry = alchemy_db.session.query(Job.id, Job.status, Job.location, Job.data).filter(Job.id == jobId).first()

			data = {'data': {'id': entry[0],
						'status': entry[1],
						'location': entry[2],
						'data': entry[3]
						}
					}
			return '{}'.format(json.dumps(data))
		elif request.method == 'DELETE':
			alchemy_db.session.query(Job.id, Job.status, Job.location, Job.data).filter(Job.id == jobId).delete()
			alchemy_db.session.commit()

	entries = alchemy_db.session.query(Job.id, Job.status, Job.location, Job.data).all()
	data = {}
	for entry in entries:
		data[entry[0]] = {
			'status': entry[1],
			'location': entry[2],
			'links': {
				'run query': 'http://127.0.0.1:5000/run/{}'.format(entry[0]),
				'view data': 'http://127.0.0.1:5000/job/{}'.format(entry[0])
			}
		}

	return '{}'.format(json.dumps(data))

@qwer.route('/run/<jobId>', methods=['GET'])
def run_job(jobId):
	entry = alchemy_db.session.query(Job.id, Job.status, Job.location, Job.data).filter(Job.id == jobId).first()
	add_to_queue(jobId, entry[2])

	return 'Job added to queue: {}'.format(jobId)

############
# QUEUEING #
############

def add_to_queue(jobId, location):

	connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	channel = connection.channel()
	channel.queue_declare(queue='jobs')

	channel.basic_publish(exchange='',
	                      routing_key='jobs',
	                      body='{} {}'.format(jobId, location))
	connection.close()

if __name__ == '__main__':
    connect_to_db(qwer)
    qwer.run()
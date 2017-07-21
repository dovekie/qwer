import os
import sqlite3
import json
import requests
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

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
		db = get_db()
		db.execute('INSERT INTO jobs (status, location) values (?, ?)', ['new', request.form['location']])
		db.commit()
		return redirect(url_for('show_jobs'))
	if jobId:
		if request.method == 'GET':
			db = get_db()
			cursor = db.execute('SELECT id, status, location, data FROM jobs WHERE id = (?)', [jobId])
			entries = cursor.fetchall()
			data = {}
			for entry in entries:
				data = {'data': {'id': entry[0],
						'status': entry[1],
						'location': entry[2],
						'data': entry[3]
						}
					}
			return '{}'.format(json.dumps(data))
		elif request.method == 'DELETE':
			db = get_db()
			db.execute('DELETE FROM jobs WHERE id = (?)', [jobId])
			db.commit()

	db = get_db()
	cursor = db.execute('SELECT id, status, location, data FROM jobs ORDER BY id DESC')
	entries = cursor.fetchall()
	data = {}
	for entry in entries:
		data[entry['id']] = {
			'status': entry['status'],
			'location': entry['location'],
			'links': {
				'run query': 'http://127.0.0.1:5000/run/{}'.format(entry['id']),
				'view data': 'http://127.0.0.1:5000/job/{}'.format(entry['id'])
			}
		}

	return '{}'.format(json.dumps(data))

@qwer.route('/run/<jobId>', methods=['GET'])
def run_job(jobId):
	db = get_db()
	cursor = db.execute('SELECT location FROM jobs WHERE id = (?)', [jobId])
	entries = cursor.fetchall()
	q = MasterQueue()
	for entry in entries:
		q.add_to_q(jobId, entry[0])
		
	return 'Job added to queue: {}'.format(jobId)

############
# QUEUEING #
############

class MasterQueue(object):

	def __new__(cls):
		# This makes sure we only have one MasterQueue
		if not hasattr(cls, 'instance'):

			cls.instance = super(MasterQueue, cls).__new__(cls)

		return cls.instance

	q = Queue(maxsize=0) # if maxsize is less than one, the queue has no maximum size

	def add_to_q(jobId, location):
		q.put((jobId, location))


#######################
# DATABASE CONNECTION #
#######################

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(qwer.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    db = get_db()
    with qwer.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@qwer.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@qwer.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

if __name__ == '__main__':
    qwer.run()
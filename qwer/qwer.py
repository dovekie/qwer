import os
import sqlite3
import json
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

@qwer.route('/job', methods=['GET'])
def show_jobs():
	""" Get jobs from the queue """
	db = get_db()
	cursor = db.execute('SELECT id, status, location FROM jobs ORDER BY id DESC')
	entries = cursor.fetchall()

	return 'I found a thing! {}'.format(entries[0])

@qwer.route('/job', methods=['POST'])
def start_job():
	""" Add a job to the queue """
	db = get_db()
	db.execute('INSERT INTO jobs (status, location) values (?, ?)', ['new', request.form['location']])
	db.commit()
	return redirect(url_for('show_jobs'))

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
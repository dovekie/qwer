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

@qwer.route('/')
def index():
	resp = {'data': {},
			'links': {'self': 'http://127.0.0.1:5000/',
					  'start a job': 'http://127.0.0.1:5000/job',
					  'check job status': 'http://127.0.0.1:5000/job?id=[id]'
					  }
			}
	return json.dumps(resp)

@qwer.route('/job')
def start_job():
	""" Add a job to the queue """
	return 'this is where you would upload a job'

#######################
# DATABASE CONNECTION #
#######################

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

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
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


if __name__ == '__main__':
    qwer.run()
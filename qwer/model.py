from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    status = db.Column(db.String(64), nullable=False)
    location = db.Column(db.Text, nullable=False)
    data = db.Column(db.Text)

    def __repr__(self):
        return '<Job id={} status={} location={}>'.format(self.id, self.status, self.location)

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    print "I'm connecting to the db!"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qwer.db'
    db.app = app
    db.init_app(app)
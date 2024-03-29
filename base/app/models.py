from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(64)) # admin and regular
    gender = db.Column(db.String(16),nullable=True)
    bio = db.Column(db.String(1000),nullable=True)
    phone_no = db.Column(db.Integer,nullable=True)
    resume_loc = db.Column(db.String(1000),default='')
    keywords = db.Column(db.Text(), nullable=True, default='')


    def __repr__(self):
        return '<User {}>'.format(self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def serialize(self):
        return {'id': self.id,
                'role': self.role,
                'gender': self.gender,
                'bio': self.bio,
                'phone_no': self.phone_no,
                'stars': self.stars,
                'keywords': self.keywords,
                'applications' : [a.serialize() for a in self.applications]}


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sent = db.Column(db.String(120), db.ForeignKey('user.email'))
    received = db.Column(db.String(120), db.ForeignKey('user.email'))
    feedback_msg = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return '<Feedback {}>'.format(self.received)

    def serialize(self):
        return{'id':self.id,
                'sent':self.sent,
                'received':self.received,
                'feedback_msg': self.feedback.msg}




class JobPost(db.Model):
    __tablename__ = 'jobpost'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), db.ForeignKey('user.email'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    title = db.Column(db.String(64))
    organization = db.Column(db.String(32))
    description = db.Column(db.String(1000))
    pay = db.Column(db.FLOAT(precision=10, scale=2))
    pay_frequency = db.Column(db.String(32))
    impressions = db.Column(db.Text(), default='')
    keywords = db.Column(db.Text(), nullable=True)
    # start_date = db.Column(db.Date,nullable=True)
    # end_date = db.Column(db.Date,nullable=True)

    def __repr__(self):
        return '<Job {}>'.format(self.title, self.email)

    def serialize(self):
        return {'id': self.id,
                'email': self.email,
                'title': self.title,
                'timestamp': self.timestamp,
                'organization': self.organization,
                'description': self.description,
                'pay': self.pay,
                'pay_frequency': self.pay_frequency,
                'impressions': self.impressions,
                'keywords': self.keywords
                #'applications': [a.serialize() for a in self.applications]}
                }

class Application(db.Model):
    __tablename__ = 'application'
    id = db.Column(db.Integer, primary_key=True)
    jobpost_id = db.Column(db.Integer, db.ForeignKey('jobpost.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    status = db.Column(db.String(32))
    reject_reason = db.Column(db.String(32), default='')
    feedback_given = db.Column(db.String(32), default='No')

    def __repr__(self):
        return '<Application {}>'.format(self.id)

    def serialize(self):
        return {'id': self.id,
                'jobpost_id': self.jobpost_id,
                'user_id': self.user_id,
                'timestamp': self.timestamp,
                'status': self.status}

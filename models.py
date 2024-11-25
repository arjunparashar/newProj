from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash

db=SQLAlchemy()

class Customer(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(32),unique=True,nullable=False)
    passhash = db.Column(db.String(512),nullable=False)
    name=db.Column(db.String(64),nullable=True)
    address=db.Column(db.String(512),nullable=False)
    pincode=db.Column(db.Integer(),nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.passhash=generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.passhash,password)

class Professional(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(32),unique=True,nullable=False)
    passhash = db.Column(db.String(512),nullable=False)
    name=db.Column(db.String(64),nullable=True)
    servicetype = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    def check_password(self,password):
        return check_password_hash(self.passhash,password)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=True)
    price = db.Column(db.Integer(), nullable=False)
    timerequired=db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    # services = db.relationship("ServiceRequest",foreign_keys=[id])


class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer,db.ForeignKey('service.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    professional_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    reqdate=db.Column(db.DateTime,nullable=False)
    compdate=db.Column(db.DateTime)
    servicestatus = db.Column(db.String(50), nullable=False)
    remarks = db.Column(db.String(50), nullable=False)
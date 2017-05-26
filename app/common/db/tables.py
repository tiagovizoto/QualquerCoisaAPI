from app import app, db
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base


class Job(db.Model):

    __tablename___ = "job"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    url_job = db.Column(db.String(255))
    name_business = db.Column(db.String(255))
    location = db.Column(db.String(144))
    email = db.Column(db.String(144))
    website = db.Column(db.String(100))
    modality = db.Column(db.String(10))
    employment_contract = db.Column(db.String(40))
    salary = db.Column(db.Float(10, 2))
    slug = db.Column(db.String(255))
    date_pub = db.Column(db.DateTime)

    def __init__(self, title, description,name_business,location,email,website,modality,salary,employment_contract,url_job=None):
        self.email = email
        self.description = description
        self.employment_contract = employment_contract
        self.location = location
        self.modality = modality
        self.title = title
        self.salary = salary
        self.website = website
        self.name_business = name_business
        if url_job is not None:
            self.url_job = url_job
        self.date_pub = datetime.utcnow()

    def __repr__(self):
        return '<Job %r>' % self.title


class Applicant(db.Model):

    __tablename__ = 'applicant'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(200))
    date_apply = db.Column(db.DateTime)
    message = db.Column(db.Text)
    fk_job = db.Column(db.Integer, db.ForeignKey('job.id'))

    def __init__(self, name, email,id_job, message=None):
        self.email = email
        self.name = name
        self.fk_job = id_job
        self.date_apply = datetime.utcnow()
        if message is not None:
            self.message = message

    def __repr__(self):
        return '<Applicant %r>' % self.name


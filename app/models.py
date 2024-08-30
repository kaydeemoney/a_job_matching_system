from . import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.Enum('recruiter', 'seeker'), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    recruiter_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    degree = db.Column(db.String(100))
    experience = db.Column(db.Integer)
    tech_skills = db.Column(db.Text)
    soft_skills = db.Column(db.Text)
    teamwork = db.Column(db.Boolean)
    cv_required = db.Column(db.Boolean)
    salary_range = db.Column(db.String(50))
    role = db.Column(db.String(100))

class Application(db.Model):
    __tablename__ = 'applications'
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=True)
    job_title = db.Column(db.String(500), nullable=False)
    seeker_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    status = db.Column(db.Enum('unreviewed', 'accepted', 'rejected', 'invited'), default='unreviewed')
    invite_details = db.Column(db.Text, nullable=True)
    academic_qual = db.Column(db.String(500), nullable=False)
    work_experience = db.Column(db.String(500), nullable=False)
    apply_letter = db.Column(db.String(500), nullable=False)
    tech_skills = db.Column(db.String(100), nullable=False)
    soft_skills = db.Column(db.String(500), nullable=False)
    tma = db.Column(db.String(1), nullable=False)
    cv = db.Column(db.Boolean, nullable=False)
    asking_salary = db.Column(db.String(15), nullable=False)



class ReportAndVerdict(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    seeker_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum('unreviewed', 'reviewed', default='reviewed'), nullable=False)
    admin_verdict = db.Column(db.Text, nullable=False)
    accepted_or_declined = db.Column(db.Boolean, nullable=False)
    work_experience = db.Column(db.String(500), nullable=False)
    apply_letter = db.Column(db.String(500), nullable=False)
    tech_skills = db.Column(db.String(100), nullable=False)
    soft_skills = db.Column(db.String(500), nullable=False)
    tma = db.Column(db.String(1), nullable=False)
    asking_salary = db.Column(db.String(15), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)





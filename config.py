import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '3xaq0CMQqO!/1mhq'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://fabamise:fabamise@localhost/job_matching_system.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app/static/uploads')
    ALLOWED_EXTENSIONS = {'pdf'}

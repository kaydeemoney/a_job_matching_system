from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Set the upload folder path
    app.config['UPLOAD_FOLDER'] = os.path.join(app.instance_path, 'uploads')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'home.login'

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

        from .routes import home
        app.register_blueprint(home)

    # Add middleware to handle method override
    @app.before_request
    def method_override():
        if request.method == 'POST' and '_method' in request.form:
            method = request.form['_method'].upper()
            if method in ['PUT', 'DELETE']:
                request.environ['REQUEST_METHOD'] = method
                request.environ['werkzeug.request'] = method

    return app

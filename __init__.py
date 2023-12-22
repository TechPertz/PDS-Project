from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_TYPE'] = 'filesystem'

    db.init_app(app)
    migrate.init_app(app, db)
    Session(app)

    from myapp.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from myapp.routes.profile import bp as profile_bp
    app.register_blueprint(profile_bp, url_prefix='/profile')

    from myapp.routes.service_location import bp as service_location_bp
    app.register_blueprint(service_location_bp, url_prefix='/service_location')

    from myapp.routes.device import bp as device_bp
    app.register_blueprint(device_bp, url_prefix='/device')

    from myapp.routes.energy import bp as energy_bp
    app.register_blueprint(energy_bp, url_prefix='/energy')

    from myapp.routes.event import bp as event_bp
    app.register_blueprint(event_bp, url_prefix='/event')

    from myapp.routes.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app

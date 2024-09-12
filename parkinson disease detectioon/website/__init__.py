from flask import Flask
from flask_mysqldb import MySQL


def create_app():
    app = Flask(__name__,static_url_path='/static')
    app.config['SECRET_KEY'] = 'ncigaiucfvu gchjbhcvhdc'
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'system'
    app.config['MYSQL_DB'] = 'parkinson'
    
    

    from .views import views_bp
    from .auth import auth_bp

    app.register_blueprint(views_bp)
    app.register_blueprint(auth_bp)
    
    
    return app

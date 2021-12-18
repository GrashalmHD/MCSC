import flask as fl
import sys
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():

    app = fl.Flask(__name__)

    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config['SECRET_KEY'] = 'sqlite3SecretKeyForThisApplicationWhichIsSuperSecret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from dataModels import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    from dataModels import User

    from main import main
    app.register_blueprint(main)
    
    from auth import auth as customLogin
    app.register_blueprint(customLogin)
    
    from status.statusBP import statusBP
    app.register_blueprint(statusBP)
    
    from console.console import consoleBP
    app.register_blueprint(consoleBP)
    
    from settings.settingBP import settingsBP
    app.register_blueprint(settingsBP)
    
    from lists.listsBP import listsBP
    app.register_blueprint(listsBP)
    
    from world.worldBP import worldBP
    app.register_blueprint(worldBP)
    
    from sse.sseBP import sseBP
    app.register_blueprint(sseBP)

    return app
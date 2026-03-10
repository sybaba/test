from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 注册蓝图
    from app.routes.instance_routes import instance_bp
    from app.routes.db_routes import db_bp
    from app.routes.table_routes import table_bp

    app.register_blueprint(instance_bp)
    app.register_blueprint(db_bp)
    app.register_blueprint(table_bp)

    return app
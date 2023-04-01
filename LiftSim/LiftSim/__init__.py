from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    from .index import index
    app.register_blueprint(index)

    return app

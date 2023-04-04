from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    from .index import simulation, summary

    app.register_blueprint(simulation)
    app.register_blueprint(summary)

    return app

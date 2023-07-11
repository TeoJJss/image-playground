from flask import Flask, request
from routes.blueprint import bp


def create_app():
    app = Flask(__name__)  # flask app object

    return app


app = create_app()  # Creating the app
# Registering the blueprint
app.register_blueprint(bp, url_prefix='/')


if __name__ == '__main__':  # Running the app
    app.run()
import os
from dotenv import load_dotenv
from flask import Flask
from api.controllers import api
from api.http.errors import handle_exception


def create_app():
    app = Flask(__name__)
    app.config['TRAP_HTTP_EXCEPTIONS'] = True  # Allows to handle any Exception in the error handler.
    app.url_map.strict_slashes = False  # Allows trailing slashes at the end of the route.

    app.register_blueprint(api)
    app.register_error_handler(Exception, handle_exception)

    return app


if __name__ == '__main__':
    load_dotenv()
    flask_app = create_app()
    flask_app.run(debug=os.getenv('DEBUG') == 'true')

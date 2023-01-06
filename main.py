import os
from flask import Flask
from api.controllers import api
from api.http.errors import handle_exception


def main():
    app = Flask(__name__)
    app.config['TRAP_HTTP_EXCEPTIONS'] = True  # Allows to handle any Exception in the error handler.

    app.register_blueprint(api)
    app.register_error_handler(Exception, handle_exception)
    app.run(debug=os.getenv('DEBUG') == 'true')


if __name__ == '__main__':
    main()

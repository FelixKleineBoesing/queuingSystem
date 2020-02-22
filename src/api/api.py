import connexion
import pkg_resources
from flask_cors import CORS

from src.misc.config_manager import ConfigManager

config = ConfigManager()


def get_app():
    app = connexion.FlaskApp(__name__)
    path = pkg_resources.resource_filename("src", "api/swagger.yml")
    app.add_api(path)
    CORS(app.app)
    return app


def run_app(app):
    host = config.get_value("APP_HOST")
    port = config.get_value("APP_PORT")
    app.run(host=host, port=port, debug=True)


if __name__ == "__main__":
    app = get_app()
    host = config.get_value("APP_HOST")
    port = config.get_value("APP_PORT")
    app.run(host=host, port=port, debug=True)

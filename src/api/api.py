import connexion
from src.misc.config_manager import ConfigManager
import pkg_resources

config = ConfigManager()


def get_app():
    app = connexion.FlaskApp(__name__)
    path = pkg_resources.resource_filename("src", "api/swagger.yml")
    app.add_api(path)
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

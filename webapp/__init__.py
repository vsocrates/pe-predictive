"""Initialize app."""
from flask import Flask

def create_app():
    """Construct the core app object."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")

    # Initialize Plugins
    # no plugins

    with app.app_context():
        from . import routes

        # Register Blueprints
        app.register_blueprint(routes.main_bp)
        return app
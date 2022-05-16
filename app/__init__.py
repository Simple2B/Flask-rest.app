import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_openapi3 import OpenAPI
from flask_openapi3.models import Info
from flask_openapi3.models.security import HTTPBearer


db = SQLAlchemy()
migrate = Migrate()


def create_app(environment="development"):

    from config import config
    from app.models import (
        User,
    )

    # Instantiate app.
    info = Info(title='Skelet API', version='1.0.0')
    jwt = HTTPBearer(bearerFormat="JWT")
    securitySchemes = {"jwt": jwt}
    app = OpenAPI(__name__, securitySchemes=securitySchemes, info=info)

    # Set app config.
    env = os.environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])
    config[env].configure(app)
    app.config["VALIDATE_RESPONSE"] = True

    # Set up extensions.
    db.init_app(app)
    migrate.init_app(app, db)

    # Register bluerint
    from app.views import api_auth, api_file
    app.register_api(api_auth)
    app.register_api(api_file)

    jwt = JWTManager(app)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).one_or_none()

    return app

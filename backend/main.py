from flask import Flask
from flask_restx import Api
from backend.config import DevConfig
from backend.models import Recipe, User
from backend.exts import db
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from backend.recipes import recipe_ns
from backend.auth import auth_ns


def create_app(config):
    app = Flask(__name__)
    CORS(app)

    app.config.from_object(config)
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    api = Api(app, doc='/docs')

    api.add_namespace(recipe_ns, path="/recipes")
    api.add_namespace(auth_ns, path="/auth")

# -------------------- Swagger Models --------------------



# -------------------- Flask Shell Context --------------------

    @app.shell_context_processor
    def make_shell_context():
        return {
            "db": db,
            "Recipe": Recipe,
            "User": User
        }

# -------------------- Run App --------------------
    return app

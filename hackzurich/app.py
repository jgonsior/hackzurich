# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import logging
import sys

from flask import Flask, render_template

from hackzurich import commands, public, user, challenge
from hackzurich.user.models import User
from hackzurich.challenge.models import Challenge, Category
from hackzurich.extensions import (
    bcrypt,
    cache,
    csrf_protect,
    db,
    debug_toolbar,
    flask_static_digest,
    login_manager,
    migrate,
)


def create_dummy_data():
    User.query.delete()
    admin = User(
        username="admin",
        email="admin@example.org",
        password="testtest",
        active=True,
        is_admin=True,
    )
    db.session.add(admin)

    normal_user = User(
        username="testuser",
        email="test@example.org",
        password="testtest",
        active=True,
    )
    db.session.add(normal_user)

    category1 = Category(name="Cat 1", parent_id=None)
    id1 = db.session.add(category1)
    db.session.flush()

    category2 = Category(name="Cat 2", parent_id=category1.id)
    id2 = db.session.add(category2)

    db.session.flush()

    challenge = Challenge(
        challengename="Challenge 1",
        description="Lorem ipsum",
        active=True,
        category_id=category1.id,
    )
    db.session.add(challenge)

    challenge = Challenge(
        challengename="Challenge 2",
        description="Lorem ipsum",
        active=True,
        category_id=category1.id,
    )
    db.session.add(challenge)

    challenge = Challenge(
        challengename="Challenge 3",
        description="Lorem ipsum",
        active=False,
        category_id=category1.id,
    )
    db.session.add(challenge)

    challenge = Challenge(
        challengename="Challenge 4",
        description="Lorem ipsum",
        active=True,
        category_id=category2.id,
    )
    db.session.add(challenge)


def create_app(config_object="hackzurich.settings"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    configure_logger(app)

    with app.app_context():
        if not User.query.count():
            app.logger.info("Creating dummy db data")
            create_dummy_data()
            db.session.commit()

    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    flask_static_digest.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(challenge.views.blueprint)
    return None


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template(f"{error_code}.html"), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {"db": db, "User": user.models.User}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)

# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import babel
import logging
import sys
import datetime as dt
from datetime import timedelta
from flask import Flask, render_template
from flask_admin.contrib.sqla import ModelView

from hackzurich import commands, public, user, challenge, chat, company
from hackzurich.user.models import User
from hackzurich.challenge.models import (
    Challenge,
    Category,
    User_Challenge_Association,
    Company,
)

from hackzurich.chat.models import ChatRoom, ChatMessage

from hackzurich.extensions import (
    bcrypt,
    cache,
    csrf_protect,
    db,
    debug_toolbar,
    flask_static_digest,
    login_manager,
    migrate,
    admin,
    socketio,
)


def create_dummy_data():
    User.query.delete()
    admin = User(
        username="JoinIN Bot",
        email="admin@example.org",
        password="testtest",
        active=True,
        country="Kenia",
        is_admin=True,
    )
    db.session.add(admin)

    normal_user = User(
        username="Max Mustermann",
        email="test@example.org",
        password="testtest",
        active=True,
        country="Switzerland",
    )
    db.session.add(normal_user)

    normal_user2 = User(
        username="Maxine Musterfrau",
        email="test2@example.org",
        password="testtest",
        active=True,
        country="USA",
    )
    db.session.add(normal_user2)

    normal_user3 = User(
        username="testuser3",
        email="test3@example.org",
        password="testtest",
        active=True,
        country="Lebanon",
    )
    db.session.add(normal_user3)

    category1 = Category(name="Food", parent_id=None)
    id1 = db.session.add(category1)
    db.session.flush()

    category2 = Category(name="Energy", parent_id=category1.id)
    id2 = db.session.add(category2)

    category3 = Category(name="Transport", parent_id=category1.id)
    id2 = db.session.add(category3)

    category4 = Category(name="Health", parent_id=category1.id)
    id2 = db.session.add(category4)

    category5 = Category(name="Social", parent_id=category1.id)
    id2 = db.session.add(category5)

    db.session.flush()

    company1 = Company(name="Accenture", description="Description")
    db.session.add(company1)
    company2 = Company(name="McKinsey", description="McKinsey description")
    db.session.add(company2)
    company3 = Company(name="SmartSolation", description="McKinsey description")
    db.session.add(company3)
    db.session.flush()

    chat_room = ChatRoom.create(
        name="Ein schoener Raum", room_id="The cold and amazing shower!"
    )

    challenge = Challenge(
        challengename="The cold and amazing shower!",
        description="""
Thousands of people from all over the world already shower cold. Not only will you save energy, CO<sub>2</sub> and water but there are also many positive effects on your health connected with showering cold.  Scientists found out, that cold showers do not only relief stress and prevents depressions, but also help to develop a more robust immune response.
Find out more:
https://www.wimhofmethod.com/benefits-of-cold-showers
https://www.healthline.com/health/cold-shower-benefits#improved-metabolism


You will save:
0.5kg of CO<sub>2</sub> per shower (based on gas boilers)
Equiv. 3.3 km with an average car

Company supporting you:
3X Carbon offsets in addition
        """,
        active=True,
        category_id=category1.id,
        co2offset=0.005,
        company_id=company1.id,
        chat_room=chat_room,
    )
    db.session.add(challenge)
    chat_message = ChatMessage.create(
        user=admin, text="Welcome to the challenge!", room=chat_room
    )

    chat_room = ChatRoom.create(name="Ein schoener Raum", room_id="Obvious Outdoor")

    challenge1 = Challenge(
        challengename="Obvious Outdoor",
        description="""
The world is calling. Get out and enjoy your surroundings today. You can choose between running or cycling.
Still undecided?
Learn more: https://www.livestrong.com/article/372790-cycling-vs-running-calories/

Pick:
Run 4/8/12km
Cycle 15/30/45km
Company supporting you: Accenture!
Run: 20/20/30 kg Carbon offset
Eqvuiv. 66km/124km/200km with an average car
        """,
        active=True,
        co2offset=0.03,
        category_id=category2.id,
        company_id=company1.id,
        chat_room=chat_room,
    )
    db.session.add(challenge1)
    chat_message = ChatMessage.create(
        user=admin, text="Welcome to the challenge!", room=chat_room
    )

    chat_room = ChatRoom.create(
        name="Ein schoener Raum", room_id="Just breathe and let us care about the rest!"
    )

    challenge2 = Challenge(
        challengename="Just breathe and let us care about the rest!",
        description="""

It sounds easy, but yet it can have a great impact on your life. Today, try to find three or more moments to stop and focus on your breath for two minutes.
Why does it matter to us? We want to give something back to society and support you to relief stress and balance your mental health. We are sure it will empower you to take better care of our planet too.
Find out more: link to instruction


Challenge:
3*2 min breathing!

Company supporting you: McKinsey
20 kg of Carbon offset
Equiv. 66km with an average car
        """,
        active=True,
        co2offset=0.02,
        category_id=category3.id,
        company_id=company2.id,
        chat_room=chat_room,
    )
    db.session.add(challenge2)

    chat_message = ChatMessage.create(
        user=admin, text="Welcome to the challenge!", room=chat_room
    )

    chat_room = ChatRoom.create(
        name="Ein schoener Raum", room_id="Lower your thermostat by 1° C"
    )
    challenge3 = Challenge(
        challengename="Lower your thermostat by 1° C",
        description="""
Average Swiss household (44m^2 per person): 0.4 kg of CO<sub>2</sub> per heating day

Company supporting you: SmartSolation
10 kg of Carbon offset
        """,
        active=True,
        co2offset=0.1,
        category_id=category4.id,
        company_id=company3.id,
        chat_room=chat_room,
    )
    db.session.add(challenge3)

    chat_message = ChatMessage.create(
        user=admin, text="Welcome to the challenge!", room=chat_room
    )

    chat_room = ChatRoom.create(
        name="Ein schoener Raum", room_id="Love your clothesline!"
    )
    challenge4 = Challenge(
        challengename="Love your clothesline!",
        description="""
Wash a load of laundry washed and dry it on a clothesline.
Find out more: https://www.theguardian.com/environment/ethicallivingblog/2008/may/02/treadlightlyswitchofftumbl

CO<sub>2</sub> savings:
1.8 kg of CO<sub>2</sub>
        """,
        active=True,
        co2offset=0.018,
        category_id=category5.id,
        company_id=company3.id,
        chat_room=chat_room,
    )
    db.session.add(challenge4)

    chat_message = ChatMessage.create(
        user=admin, text="Welcome to the challenge!", room=chat_room
    )

    chat_room = ChatRoom.create(
        name="Ein schoener Raum", room_id="Food For Thought!"
    )
    challenge5 = Challenge(
        challengename="Food For Thought!",
        description="""
Thanks to the magic of data we have found a large number of sustainable recipes.
These were picked thanks their low CO<sub>2</sub> emissions per serving.
Today we suggest you cook:<br><br>

        """,
        active=True,
        co2offset=0.018,
        category_id=category1.id,
        company_id=company3.id,
        chat_room=chat_room,
    )
    db.session.add(challenge5)

    chat_message = ChatMessage.create(
        user=admin, text="Welcome to the challenge!", room=chat_room
    )

    db.session.flush()

    user_challenge_association11 = User_Challenge_Association(
        normal_user.id,
        challenge1.id,
        succeeded=True,
        done_at=dt.datetime.now() - timedelta(days=13),
        commited_to_at=dt.datetime.now() - timedelta(days=13, hours=1),
    )
    db.session.add(user_challenge_association11)

    user_challenge_association12 = User_Challenge_Association(
        normal_user.id,
        challenge1.id,
        succeeded=True,
        done_at=dt.datetime.now() - timedelta(days=13),
        commited_to_at=dt.datetime.now() - timedelta(days=13, hours=1),
    )
    db.session.add(user_challenge_association12)

    user_challenge_association12 = User_Challenge_Association(
        normal_user.id,
        challenge1.id,
        succeeded=True,
        done_at=dt.datetime.now() - timedelta(days=12),
        commited_to_at=dt.datetime.now() - timedelta(days=12, hours=1),
    )
    db.session.add(user_challenge_association12)

    for i in range(1, 8):
        user_challenge_association12 = User_Challenge_Association(
            normal_user.id,
            challenge1.id,
            succeeded=True,
            done_at=dt.datetime.now() - timedelta(days=i),
            commited_to_at=dt.datetime.now() - timedelta(days=i, hours=1),
        )
        db.session.add(user_challenge_association12)


def create_app(config_object="hackzurich.settings"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_admin(app)
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

        @app.template_filter("datetime")
        def format_datetime(value, format="medium"):
            if format == "full":
                format = "EEEE, d. MMMM y 'at' HH:mm"
            elif format == "medium":
                format = "EE dd.MM.y HH:mm"
            return babel.dates.format_datetime(value, format)

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
    admin.init_app(app)
    socketio.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(challenge.views.blueprint)
    app.register_blueprint(company.views.blueprint)
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


def register_admin(app):
    """Register admin interface."""
    from hackzurich.user.models import User
    from hackzurich.challenge.models import (
        Challenge,
        Category,
        Company,
        User_Challenge_Association,
    )
    from hackzurich.chat.models import ChatMessage, ChatRoom

    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Challenge, db.session))
    admin.add_view(ModelView(Category, db.session))
    admin.add_view(ModelView(ChatRoom, db.session))
    admin.add_view(ModelView(ChatMessage, db.session))
    admin.add_view(ModelView(Company, db.session))
    admin.add_view(ModelView(User_Challenge_Association, db.session))
    app.config["FLASK_ADMIN_SWATCH"] = "cerulean"


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)

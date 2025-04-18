from datetime import timedelta
import os
import logging
from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv
from extensions import db, mail  # Import db and mail from extensions
from chatbot_routes import chatbot_routes_bp
from flight_status_updater import init_flight_status_updater  # Import the updater initializer

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv("SESSION_SECRET", "dev_secret_key")

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///flight_booking.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_recycle": 300, "pool_pre_ping": True}
app.config['SESSION_TYPE'] = 'filesystem'  
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

# Initialize SQLAlchemy with the app
db.init_app(app)

# Flask-Mail configuration
app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_DEFAULT_SENDER=os.getenv("MAIL_USERNAME"),
)

# Initialize Flask-Mail with the app
mail.init_app(app)

# Debugging email credentials (REMOVE in production)
# logging.debug(f"MAIL_USERNAME: {app.config['MAIL_USERNAME']}")
# logging.debug(f"MAIL_PASSWORD: {app.config['MAIL_PASSWORD']}")

# Import models AFTER initializing db
with app.app_context():
    from models import User  # Ensure models are imported within app context
    db.create_all()  # Optional: create tables if they don’t exist

    # Initialize and start the flight status updater
    flight_status_updater = init_flight_status_updater(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "routes.login"  # Use blueprint endpoint
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register Blueprint
from routes import routes_bp
app.register_blueprint(routes_bp)
app.register_blueprint(chatbot_routes_bp)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
import threading
import time
from datetime import datetime
import logging
from flask import current_app
from extensions import db
from models import Flight

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class FlightStatusUpdater:
    def __init__(self, app, check_interval=3600):
        """
        Initialize the flight status updater.
        
        :param app: Flask application instance
        :param check_interval: Time (in seconds) between status checks (default: 3600 seconds)
        """
        self.app = app
        self.check_interval = check_interval
        self.running = False
        self.thread = None

    def update_flight_statuses(self):
        """
        Check all scheduled flights and update their status to 'Completed' if departure time has passed.
        """
        with self.app.app_context():
            try:
                current_time = datetime.utcnow()
                logger.info(f"Checking flight statuses at {current_time}")

                # Query all flights with status "Scheduled"
                scheduled_flights = Flight.query.filter_by(status="Scheduled").all()

                updated_flights = []
                for flight in scheduled_flights:
                    if flight.departure_time <= current_time:
                        flight.status = "Completed"
                        updated_flights.append(flight.flight_number)
                        logger.info(f"Updated flight {flight.flight_number} status to 'Completed'")

                if updated_flights:
                    db.session.commit()
                    logger.info(f"Updated {len(updated_flights)} flights: {', '.join(updated_flights)}")
                else:
                    logger.info("No flights needed status updates")

            except Exception as e:
                logger.error(f"Error updating flight statuses: {str(e)}")
                db.session.rollback()

    def run(self):
        """
        Run the updater in a loop until stopped.
        """
        self.running = True
        while self.running:
            self.update_flight_statuses()
            time.sleep(self.check_interval)

    def start(self):
        """
        Start the flight status updater thread.
        """
        if not self.running and self.thread is None:
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()
            logger.info("Flight status updater thread started")
            return self.thread
        else:
            logger.warning("Flight status updater is already running")
            return None

    def stop(self):
        """
        Stop the flight status updater thread.
        """
        if self.running:
            self.running = False
            if self.thread:
                self.thread.join()
                self.thread = None
            logger.info("Flight status updater thread stopped")

def init_flight_status_updater(app):
    """
    Initialize and start the flight status updater with the Flask app.
    
    :param app: Flask application instance
    :return: FlightStatusUpdater instance
    """
    updater = FlightStatusUpdater(app, check_interval=3600)  # Check every 3600 seconds
    updater.start()
    return updater 
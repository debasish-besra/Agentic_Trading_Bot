import logging
import os
from datetime import datetime

# Create 'logs/' directory in your current working directory if it doesn't exist
LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)  # Safe to run even if 'logs/' already exists

# Create a unique log file with current date and time (so logs don't overwrite)
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE)

# Configure logging settings
logging.basicConfig(
    filename=LOG_FILE_PATH,  # Log to this file

    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",  # Format: timestamp, line number, module name, log level, actual message
    level=logging.INFO,  # Only log INFO and above (INFO, WARNING, ERROR, CRITICAL)
)

# Create a logger instance with a custom name for your agentic app
logger = logging.getLogger("my_agentic_app")


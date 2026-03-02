import sys
import os
import logging
import traceback

# Configure logging before anything else
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add src/ to path
src_path = os.path.join(os.path.dirname(__file__), "..", "src")
logger.info(f"Adding to sys.path: {src_path}")
sys.path.insert(0, src_path)

# Debug: print directory structure
logger.info(f"api/ directory: {os.listdir(os.path.dirname(__file__))}")
logger.info(f"src/ path exists: {os.path.exists(src_path)}")
if os.path.exists(src_path):
    logger.info(f"src/ directory: {os.listdir(src_path)}")

try:
    logger.info("Importing Flask app from src/app.py")
    from app import app
    logger.info("Successfully imported Flask app")
except Exception as e:
    logger.error(f"Failed to import app: {e}")
    logger.error(traceback.format_exc())

    # Create a fallback error app
    from flask import Flask
    app = Flask(__name__)

    @app.route('/')
    def error():
        return f"Import Error: {e}\n\n{traceback.format_exc()}", 500

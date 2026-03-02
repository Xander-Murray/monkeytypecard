import sys
import os
import logging

# Configure logging before anything else
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add src/ to path
src_path = os.path.join(os.path.dirname(__file__), "..", "src")
logger.info(f"Adding to sys.path: {src_path}")
sys.path.insert(0, src_path)

try:
    logger.info("Importing Flask app from src/app.py")
    from app import app
    logger.info("Successfully imported Flask app")
except Exception as e:
    logger.error(f"Failed to import app: {e}", exc_info=True)
    raise

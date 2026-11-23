from utils.logger import setup_logger

logger = setup_logger()

logger.info("Triton application started")
logger.warning("Test warning")
logger.error("Test error")
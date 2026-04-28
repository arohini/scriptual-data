import logging
import functools

# Basic configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_execution(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
        logger.info(f"starting execution of {func.__name__} at {logging.Formatter.formatTime(logging.Formatter(), None)}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"{func.__name__} returned: {result}")
            logger.info(f"Completed execution of {func.__name__} at {logging.Formatter.formatTime(logging.Formatter(), None)}")
            return result
        except Exception as e:
            logger.exception(f"Exception in {func.__name__}: {e}")
            raise
    return wrapper

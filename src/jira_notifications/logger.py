import logging
import threading
import traceback

class LogFormatter(logging.Formatter):
    """A custom log formatter for colored console output.

    This formatter adds color coding to log messages based on their log level.

    Attributes:
        
        grey (str): ANSI escape code for grey color.
        green (str): ANSI escape code for green color.
        yellow (str): ANSI escape code for yellow color.
        red (str): ANSI escape code for red color.
        bold_red (str): ANSI escape code for bold red color.
        reset (str): ANSI escape code to reset text color to default.
        white (str): ANSI escape code for white color.
        log_format (str): The format of log messages.
        FORMATS (dict): A dictionary that maps log levels to their respective log formats.
    :no-index:
    """
    grey = '\x1b[32;1m'
    green = '\x1b[32;1m'
    yellow = "\x1b[33;20m"
    red = '\x1b[31;20m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'
    white = "\x1b[37m"
    log_format = '%(asctime)s - %(filename)s - %(levelname)s - %(message)s'
    error_log_format = (
        '%(asctime)s - %(filename)s - %(lineno)d - %(levelname)s - %(message)s'
    ) # Include lineno

    FORMATS = {
        logging.DEBUG: grey + log_format + reset,
        logging.INFO: white + log_format + reset,
        logging.WARNING: yellow + log_format + reset,
        logging.ERROR: red + error_log_format + reset,
        logging.CRITICAL: bold_red + log_format + reset
    }

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record with color-coded log level.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log message with color coding.
        """
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        if record.levelno == logging.ERROR:
            exc_info = record.exc_info
            if exc_info:
                # Include the traceback in the log message
                traceback_text = "\n".join(traceback.format_exception(*exc_info))
                record.msg += "\n" + traceback_text
        return formatter.format(record)



class ThreadSafeLogger(logging.Logger):
    """ this class take care of thread safe logging"""
    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)
        self.lock = threading.Lock()

    def handle(self, record):
        with self.lock:
            super().handle(record)

def get_logger(filename, log_level=logging.INFO):
    """Get a configured logger for the specified filename.

    Retrieves a logger instance configured with a specified log level and log format.

    Args:
        filename (str): The name of the logger (e.g., filename or module name).
        log_level (int, optional): The log level for the logger (default is logging.INFO).

    Returns:
        logging.Logger: A configured logger instance.
    """
    filename = filename if filename else 'root'
    log = ThreadSafeLogger(filename, log_level)
    log.propagate = False

    ch = logging.StreamHandler()
    ch.setFormatter(LogFormatter())
    log.addHandler(ch)
    return log
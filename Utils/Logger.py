import logging
import sys
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

# Define color mappings
LOG_COLORS = {
    "DEBUG": Fore.BLUE,
    "INFO": Fore.GREEN,
    "WARNING": Fore.YELLOW,
    "ERROR": Fore.RED,
    "CRITICAL": Fore.RED + "\033[1m",  # Bold red
}

class ColoredFormatter(logging.Formatter):
    def format(self, record):
        log_color = LOG_COLORS.get(record.levelname, Fore.WHITE)
        log_msg = super().format(record)
        return f"{log_color}{log_msg}{Fore.RESET}"

def get_logger(name="MyLogger"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Create a console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    # Define log format
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = ColoredFormatter(log_format)

    # Apply formatter to handler
    console_handler.setFormatter(formatter)

    # Add handler to logger
    if not logger.hasHandlers():  # Prevent adding multiple handlers
        logger.addHandler(console_handler)

    return logger
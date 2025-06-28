import logging
import sys

def setup_logger():
    """
    Configures the root logger for the application.
    """
    # Define the format for our log messages
    log_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(module)s - %(message)s'
    )

    # --- Create a handler to write logs to a file ---
    # This will rotate the log file, keeping a backup when it reaches 2MB.
    file_handler = logging.FileHandler("phishing_detector.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(log_format)

    # --- Create a handler to print logs to the console ---
    # This is useful so we can still see output in the terminal while running.
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)

    # --- Get the root logger and add our handlers ---
    # We configure the root logger so we can get it by name in other modules.
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Avoid adding handlers multiple times if this function is called again
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
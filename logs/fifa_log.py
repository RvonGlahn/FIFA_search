import logging
import sys

def fifa_logger():
    # set logger and global logging threshold
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # StreamHandler for shell
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    # FileHandler for File
    file_handler = logging.FileHandler('fifa.log')
    file_handler.setLevel(logging.WARNING)

    # Create Formatter
    stream_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # set formatter in handler
    stream_handler.setFormatter(stream_format)
    file_handler.setFormatter(file_format)

    # Add Handler to logger
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    
    return logger


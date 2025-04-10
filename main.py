import pyskindose
from logging_config import configure_module_logging
import logging

if __name__ == "__main__":
    logger = logging.getLogger('main')
else:
    logger = logging.getLogger(__name__)






def main():
    """the main function to run the script"""
    logger.info('Starting the main function')





if __name__ == '__main__':
    configure_module_logging({
        'main': {'file': 'main.log', 'level': logging.DEBUG, 'console': True}}
    )
    main()
from dotenv import load_dotenv
from datetime import datetime
import logging
import os

class ENV:
    @staticmethod
    def init_config():
        try:
            load_dotenv('.env')
            # Set up logging
            log_dir = "logs"
            log_filename = os.path.join(log_dir, f"script_log_{datetime.now().strftime('%Y%m%d')}.log")
            logging.basicConfig(
                level=logging.INFO,  # You can set this to DEBUG, INFO, WARNING, ERROR, CRITICAL
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler(log_filename),
                    # logging.StreamHandler()  # Uncomment this line to also log to the console
                ]
            )
        except Exception as e:
            raise Exception("Error loading .env file, make sure you have a .env file in the root directory") from e

    @staticmethod
    def get(var_name):
        value = os.getenv(var_name)
        if value is None:
            load_dotenv('.env')
            value = os.getenv(var_name)
            if value is None:
                raise Exception(f"Error loading {var_name} from .env file")
        return value

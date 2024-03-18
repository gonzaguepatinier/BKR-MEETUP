import logging
import json


global logger

def init_logger(logger_name: str, logger_file_name):


    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # Handler for console output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Handler for file output
    file_handler = logging.FileHandler(logger_file_name)
    file_handler.setLevel(logging.DEBUG)

    # Formatter for log messages
    formatter = logging.Formatter('[%(asctime)s] %(levelname)-8s %(message)s')

    # Add formatters to handlers
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

def get_site_credentials(site_credential_file: str):

    # Opening JSON file
    Username = ''
    Password = ''
    logger.debug('Site: Fetching Credentials')

    f = open(site_credential_file)

    # returns JSON object as
    # a dictionary
    data = json.load(f)

    # Iterating through the json
    # list
    index=0
    for i in data['user_credentials']:
        Username = (i['username'])
        Password = (i['password'])

    # logger.debug(f'Site: Username: {Username}')
    # logger.debug(f'Site: Password: {Password}')

    # Closing file
    f.close()
    return Username, Password

    if __name__ == "__main__":
        main()
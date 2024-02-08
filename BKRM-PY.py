#
# BKRM-PY.py
#
#
# TODO: search for keywords


# DONE:
# - store data in database sqlite
# - List all job related (recurse until last pages)
# - Stored in Dataframe / XLS / CSV or JSON File
# - Extract

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
import os
import logging
import json
import time
import pandas as pd
from urllib.parse import urlparse, urlencode, parse_qs, urlunparse
import sqlite3

BKRM_HOME_DIR = "/Users/gonzaguepatinier/Documents/GitHub/BKR-MEETUP/"
BKRM_DB = BKRM_HOME_DIR + "./BKRM_data.db'"
DF_DATA_FILE = BKRM_HOME_DIR + './BKRM_DF_Data_File.csv'

BKRM_JOB_URL = "https://th.jobsdb.com/th/en/job/job-300003002885733"
BKRM_LOGGER = 'my_logger_BKRM'
BKRM_LOGGER_FILE = BKRM_HOME_DIR + './BKRM_my_log_file.log'
BKRM_CREDENTIALS_FILE = 'BKRM-Credentials.json'
BKRM_TABLE_NAME = 'BKRM'
BKRM_LOGIN_PAGE = "https://www.meetup.com/login/"
BKRM_SITE = "BKRM"

df = pd.DataFrame(
            [],
            columns=['event_site',
                     'event_date',
                     'event_title',
                     'event_organizer',
                     'event_attendee_number',
                     'event_url'] )



# Initialise Logging

def Init_Logger(logger_name: str, logger_file_name):
    global logger

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



# Load username/password from local file

def scroll_to_bottom(driver):
    # Scroll to the bottom of the page using JavaScript
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)  # Adjust the sleep time as needed

def Site_Credentials(site_credential_file: str):

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

    logger.debug(f'Site: Username: {Username}')
    logger.debug(f'Site: Password: {Password}')

    # Closing file
    f.close()
    return Username, Password

def Site_login(local_webdriver: webdriver, site_login_page: str, Username: str, Password: str):

    logger.debug('Site: Login Page')
    local_webdriver.get(site_login_page)

    logger.debug('Site: Insert Username')

    xpath_username = "email" # id

    username = local_webdriver.find_element("id", xpath_username )
    username.send_keys(Username)

    logger.debug('Site: Insert Password')

    xpath_password = "current-password" # id
    pword = local_webdriver.find_element("id",xpath_password)
    pword.send_keys(Password)

    logger.debug('Site: Click Submit')
    xpath_button = "submitButton" # id
    local_webdriver.find_element("name",xpath_button).click()


    # End of Function


def Site_Extract_Event_Details(local_webdriver: webdriver, url_event: str) -> str:

    global df

    local_webdriver.get(url_event)

    logger.debug('BKRM: Extract Data from event')
    logger.debug(f'BKRM: URL {url_event}')

    # xpath_organizer = "//a[@data-event-label='hosted-by']"
    # xpath_organizer = "//a[@id='hosted-by']"
    # run_organizer_element= local_webdriver.find_element("xpath",xpath_organizer)
    id_organizer = "hosted-by"
    run_organizer_element= local_webdriver.find_element("id",id_organizer)

    run_organizer_intermediate= run_organizer_element.get_attribute("aria-label")
    print(run_organizer_intermediate)

    if run_organizer_intermediate is not None:
        run_organizer_text = run_organizer_intermediate[10:]
    else:
       run_organizer_text = "No Organizer"

    print (f"Organizer: {run_organizer_text}")

    logger.debug(f'Event Organizer: {run_organizer_text}')

    return (run_organizer_text)

def print_element_attributes(element: WebElement):
    all_attributes = element.get_property("attributes")

    # Iterate through the dictionary and print each attribute and its value
    for attribute in all_attributes:
        attribute_name = attribute["name"]
        attribute_value = element.get_attribute(attribute_name)
        print(f"{attribute_name}: {attribute_value}")

def Site_Extract_Cal_Event(local_webdriver: webdriver, local_event_webdriver: webdriver, url_site: str, iteration: int):

    global df

    local_webdriver.get(url_site)

    logger.debug('BKRM: Extract Data from current page')
    logger.debug('BKRM: Extract URLs')

    # Sroll the infinite loop a few times

    for index in range(1,iteration):
        logger.debug(f'BKRM: scrolling [{str(index)}]')
        scroll_to_bottom(local_webdriver)

    # Search for WebElement for each event

    xpath_event = '//*[starts-with(@id, "ep-")]'
    div_elements = local_webdriver.find_elements("xpath",xpath_event)

    element_index = 1

    for element in div_elements:

        element_index_text = "{:02d}".format(element_index)
        logger.debug(f"ELEMENT [{element_index_text}] : ")

        # Search for time of event

        xpath_time = ".//time"
        run_time = element.find_element("xpath",xpath_time)
        logger.debug(f"BKRM: Time: {run_time.text}")

        # Search for URL of full event description
        # Used to extract organiser

        xpath_meetup_url_link = ".//a[@class='flex h-full flex-col justify-between space-y-5 outline-offset-8 hover:no-underline']"
        run_meetup_url_link = element.find_element("xpath",xpath_meetup_url_link)
        run_meetup_url_link_text = run_meetup_url_link.get_attribute("href")
        logger.debug(f"BKRM: Meetup url link: {run_meetup_url_link_text}")

        # Search for Event Title

        xpath_title = './/span[@class="ds-font-title-3 block break-words leading-7 utils_cardTitle__lbnC_ text-gray6"]'
        run_title = element.find_element("xpath",xpath_title)
        logger.debug(f"BKRM: Title: {run_title.text}")

        # Search for attendee number
        # in some event, no attendee is written

        xpath_attendee_number = ".//span[@class='hidden sm:inline']"
        try:
            run_attendee_number = element.find_element("xpath",xpath_attendee_number)
            run_attendee_number_text_temp= run_attendee_number.text
            an_text = run_attendee_number_text_temp.split()
            run_attendee_number_text = an_text[0]
            logger.debug(f"BKRM: Attendee Number: {run_attendee_number.text}")

        except NoSuchElementException:
            run_attendee_number_text= "0"

        # Search for organizer name from details event description

        run_organizer = Site_Extract_Event_Details(local_event_webdriver, run_meetup_url_link_text)

        # run_organizer = "BKK RUNNERS"

        element_index = element_index +1

        # Create a new record to add
        new_record = {'event_site':BKRM_SITE,
                    'event_date': run_time.text,
                    'event_title': run_title.text,
                    'event_organizer': run_organizer,
                    'event_attendee_number': run_attendee_number_text,
                    'event_url': run_meetup_url_link_text}

        # Append the new record to the DataFrame
        df = df.append(new_record, ignore_index=True)
        logger.debug(f'Adding Event: {run_time.text} / {run_title.text}')


def Site_Extract_Cal_Event_Max(local_webdriver: webdriver, local_event_webdriver: webdriver, url_site: str, max_event_event: int):

    global df

    local_webdriver.get(url_site)

    logger.debug('BKRM: Extract Data from current page')
    logger.debug('BKRM: Extract URLs')

    # Sroll the infinite loop a few times

    #    scroll_to_bottom(local_webdriver)

    # Search for WebElement for each event

#     # Construct the XPath expression using position()
# xpath_expression = f"//your/xpath/expression[position() >= {starting_position}]"

# # Find elements using the constructed XPath expression
# selected_elements = driver.find_elements_by_xpath(xpath_expression)
    
    starting_position = 0
    element_index = 1

    xpath_event = '//*[starts-with(@id, "ep-")]'
    div_elements = local_webdriver.find_elements("xpath",xpath_event)

    xpath_event = f'//*[starts-with(@id, "ep-")][position() >= {starting_position}]'
    div_elements = local_webdriver.find_elements("xpath",xpath_event)

    

    for element in div_elements:

        element_index_text = "{:02d}".format(element_index)
        logger.debug(f"ELEMENT [{element_index_text}] : ")

        # Search for time of event

        xpath_time = ".//time"
        run_time = element.find_element("xpath",xpath_time)
        logger.debug(f"BKRM: Time: {run_time.text}")

        # Search for URL of full event description
        # Used to extract organiser

        xpath_meetup_url_link = ".//a[@class='flex h-full flex-col justify-between space-y-5 outline-offset-8 hover:no-underline']"
        run_meetup_url_link = element.find_element("xpath",xpath_meetup_url_link)
        run_meetup_url_link_text = run_meetup_url_link.get_attribute("href")
        logger.debug(f"BKRM: Meetup url link: {run_meetup_url_link_text}")

        # Search for Event Title

        xpath_title = './/span[@class="ds-font-title-3 block break-words leading-7 utils_cardTitle__lbnC_ text-gray6"]'
        run_title = element.find_element("xpath",xpath_title)
        logger.debug(f"BKRM: Title: {run_title.text}")

        # Search for attendee number
        # in some event, no attendee is written

        xpath_attendee_number = ".//span[@class='hidden sm:inline']"
        try:
            run_attendee_number = element.find_element("xpath",xpath_attendee_number)
            run_attendee_number_text_temp= run_attendee_number.text
            an_text = run_attendee_number_text_temp.split()
            run_attendee_number_text = an_text[0]
            logger.debug(f"BKRM: Attendee Number: {run_attendee_number.text}")

        except NoSuchElementException:
            run_attendee_number_text= "0"

        # Search for organizer name from details event description

        run_organizer = Site_Extract_Event_Details(local_event_webdriver, run_meetup_url_link_text)

        # run_organizer = "BKK RUNNERS"

        element_index = element_index +1
        starting_position = starting_position + 1

        # Create a new record to add
        new_record = {'event_site':BKRM_SITE,
                    'event_date': run_time.text,
                    'event_title': run_title.text,
                    'event_organizer': run_organizer,
                    'event_attendee_number': run_attendee_number_text,
                    'event_url': run_meetup_url_link_text}

        # Append the new record to the DataFrame
        df = df.append(new_record, ignore_index=True)
        logger.debug(f'Adding Event: {run_time.text} / {run_title.text}')

def main():

    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Clear Terminal Console

    os.system('clear')
    os.chdir(BKRM_HOME_DIR)
    os.system('pwd')



    Init_Logger(BKRM_LOGGER, BKRM_LOGGER_FILE)

    logger.debug('BKRM: -----')
    logger.debug('BKRM: Start')

    Username, Password = Site_Credentials(BKRM_CREDENTIALS_FILE)

    chrome_options = webdriver.ChromeOptions()

    # Set options as needed
    chrome_options.add_argument('--headless')  # Run Chrome in headless mode (without GUI)
    chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration in headless mode

    # Specify the path to the ChromeDriver executable using ChromeDriverManager
    # driver = webdriver.Chrome(service=webdriver.ChromeService(executable_path=ChromeDriverManager().install()), options=chrome_options)

    driver_main = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
    driver_second = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)

    url_past = "https://www.meetup.com/bangkok-runners/events/?type=past"
    Site_login(driver_main, BKRM_LOGIN_PAGE,Username,Password)
    Site_login(driver_second, BKRM_LOGIN_PAGE,Username,Password)

    driver_main.get(url_past)

    # iteration = 2
    max_element = 5
    # Site_Extract_Cal_Event(driver_main,driver_second, url_past, iteration)
    Site_Extract_Cal_Event_Max(driver_main,driver_second, url_past,max_element )


    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    df.to_csv(DF_DATA_FILE, index=False)

    conn = sqlite3.connect(BKRM_DB)

    df.to_sql(BKRM_TABLE_NAME, conn, if_exists='append', index=False)
    pd.read_sql(f'select * from {BKRM_TABLE_NAME}', conn)

    logger.debug('BKRM: Completed')
    logger.debug('BKRM: -----')
    logger.debug('BKRM: END')


if __name__ == "__main__":
    main()

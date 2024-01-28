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
            columns=['job_site',
                     'job_id',
                     'job_title',
                     'job_company_name',
                     'job_location',
                     'job_date_posted',
                     'job_url'] )



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

    logger.debug('Site: Username: ' + Username)
    logger.debug('Site: Password: '+ Password)

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


# def Site_Extract_Cal_Event(local_webdriver: webdriver, url_site: str, Year: int, Month: int):
def Site_Extract_Cal_Event(local_webdriver: webdriver, url_site: str):

    global df
    
    # Month_text = result_string = "{:02d}".format(Month)
    # url = url_site + str(Year) + "-" + Month_text + "/"

    # local_webdriver.get(url)
    
    local_webdriver.get(url_site)
    


    logger.debug('JDB: Extract Data from current page')
    logger.debug('JDB: Extract URLs')

    # xpath_event = "//div[@id='ep-*']"
    xpath_event = '//*[starts-with(@id, "ep-")]'

    for i in range(1,1):
        scroll_to_bottom(local_webdriver)
    
    # scroll_to_bottom(local_webdriver)
    
    div_elements = local_webdriver.find_elements("xpath",xpath_event)                                                                                                                        

    element_index = 1

    for element in div_elements: 

        # logger.debug('JDB: Number ['+str(i) + "]")
        element_index_text = "{:02d}".format(element_index)
        print("ELEMENT [" + element_index_text + "] : ")
        # print (element.text)

        all_attributes = element.get_property("attributes")

        # Iterate through the dictionary and print each attribute and its value
        for attribute in all_attributes:
            attribute_name = attribute["name"]
            attribute_value = element.get_attribute(attribute_name)
            print(f"{attribute_name}: {attribute_value}")

        xpath_time = ".//time"
        run_time = element.find_element("xpath",xpath_time) 
        print ("Time: " + run_time.text)

        xpath_meetup_url_link = ".//a[@class='flex h-full flex-col justify-between space-y-5 outline-offset-8 hover:no-underline']"
        run_meetup_url_link = element.find_element("xpath",xpath_meetup_url_link)
        run_meetup_url_link_text = run_meetup_url_link.get_attribute("href")
        print ("Meetup url link: " + run_meetup_url_link_text)


        # xpath_title = ".//span[starts-with(@class, 'ds-font-title-3']"
        xpath_title = './/span[@class="ds-font-title-3 block break-words leading-7 utils_cardTitle__lbnC_ text-gray6"]'
        run_title = element.find_element("xpath",xpath_title)
        print ("Title: " + run_title.text)

        

        xpath_attendee_number = ".//span[@class='hidden sm:inline']"
        try:
            run_attendee_number = element.find_element("xpath",xpath_attendee_number)
            print ("Attendee Number: " + run_attendee_number.text)
        except NoSuchElementException:
            print ("Attendee Number: None")
        
        element_index = element_index +1


    # scroll_to_bottom(local_webdriver)

    # xpath_job = "//div[@class='z1s6m00 _1hbhsw67i _1hbhsw66e _1hbhsw69q _1hbhsw68m _1hbhsw6n _1hbhsw65a _1hbhsw6ga _1hbhsw6fy']"

    # div_elements = local_webdriver.find_elements("xpath",xpath_job)                                                                                                                        

    # for element in div_elements: 

    #     logger.debug('JDB: Number ['+str(i) + "]")

    #     # JOB URL

    #     job_url= element.find_element("xpath",".//a[@rel='nofollow noopener noreferrer']")   
    #     job_url_text = job_url.get_attribute("href")
    #     parsed_url = urlparse(job_url_text)

    #     # Access different components of the URL
    #     scheme = parsed_url.scheme
    #     netloc = parsed_url.netloc
    #     path = parsed_url.path
    #     query = parsed_url.query
    #     fragment = parsed_url.fragment

    #     # Parse query string into a dictionary
    #     query_params = parse_qs(parsed_url.query)
    #     # print("Query Parameters:", query_params)

    #     # Modify and rebuild the URL
    #     # modified_url = urlunparse(("https", "www.updated-example.com", "/new-path", "", "param1=new_value&param3=new_param", ""))
    #     modified_url = urlunparse((scheme, netloc, path, "", "",""))
    #     job_url_text = modified_url

    #     job_Id = query_params['jobId']
    #     job_id_text = job_Id[0]

    #     logger.debug('JDB: URL ['+str(i)+"] : "+ job_url_text) 
        
    #     # JOB TITLE

    #     title_element = element.find_element("xpath",".//div[@class='z1s6m00 im1gct0 im1gct4 im1gct2']/.//span[@class='z1s6m00']")                                                                                                                        
    #     title_element_text = title_element.text
    #     logger.debug('JDB: Title ['+str(i)+"] : "+ title_element_text)  

    #     # JOB COMPANY

    #     try:
    #         company_element = element.find_element("xpath",".//span[@class='z1s6m00 bev08l1 _1hbhsw64y _1hbhsw60 _1hbhsw6r']/.//a[@data-automation='jobCardCompanyLink']")                                                                                                                         
    #         company_element_text = company_element.text
    #     except NoSuchElementException:  #spelling error making this code not work as expected
    #         company_element_text = "Company Info Not provided"
    #         pass


    #     logger.debug('JDB: Company ['+str(i)+"] : "+ company_element_text)  

    #     # JOB POST DATE

    #     # xpath_job_posted_date = ".//span[@class='z1s6m00 _1hbhsw64y y44q7i0 y44q7i1 y44q7i22 y44q7ihi']"
    #     xpath_job_posted_date = ".//time[@class='z1s6m00 _1hbhsw64y']"
    #     job_posted_date_element = element.find_element("xpath",xpath_job_posted_date)                                                                                                                        
    #     # job_posted_date_element_text = job_posted_date_element.text
    #     job_posted_date_element_text = job_posted_date_element.get_attribute("datetime")
    #     job_posted_date_element_text = job_posted_date_element_text[0:10]
    #     logger.debug('JDB: Date ['+str(i)+"] : "+ job_posted_date_element_text)  

    #     # JOB LOCATION

    #     # xpath_job_location = ".//span[@class='z1s6m00 bev08l1 _1hbhsw64y _1hbhsw60 _1hbhsw6r']"
    #     xpath_job_location = ".//a[@data-automation='jobCardLocationLink']"
    #     job_location_element = element.find_element("xpath",xpath_job_location)                                                                                                                        
    #     job_location_element_text = job_location_element.text
    #     logger.debug('JDB: Location ['+str(i)+"] : "+ job_location_element_text)  

    #     # Job Description Summary
    #     #jobList > div.z1s6m00.iw87102 > div:nth-child(2) > div > div:nth-child(2) > div > div > article > div > div > div.z1s6m00._1hbhsw67i._1hbhsw66e._1hbhsw69q._1hbhsw68m._1hbhsw6n._1hbhsw65a._1hbhsw6ga._1hbhsw6fy > div:nth-child(1) > div.z1s6m00._1hbhsw6ba._1hbhsw64y > ul > li:nth-child(1) > div > div.z1s6m00._1hbhsw6r._1hbhsw6p._1hbhsw6a2 > span
        
    #     xpath_job_description_box = ".//div[@data-automation='job-card-selling-points']"
    #     xpath_job_description = ".//span[@class='z1s6m00 _1hbhsw64y y44q7i0 y44q7i1 y44q7i21 _1d0g9qk4 y44q7i7']"
        
    #     job_description_list = element.find_element("xpath",xpath_job_description_box)

    #     job_description_elements = job_description_list.find_elements("xpath",xpath_job_description)                                                                                                                        

    #     for job_description_element in job_description_elements:
    #         job_description_element_text = job_description_element.text
    #         logger.debug('JDB: Description ['+str(i)+"] : "+ job_description_element_text)  

    #     # Create a new record to add
    #     new_record = {'job_site':BKRM_SITE,
    #                 'job_id': job_id_text,
    #                 'job_title': title_element_text,
    #                 'job_company_name': company_element_text,
    #                 'job_location': job_location_element_text,
    #                 'job_date_posted': job_posted_date_element_text,
    #                 'job_url': job_url_text}

    #     # Append the new record to the DataFrame
    #     df = df.append(new_record, ignore_index=True)
    #     logger.debug('JDB Adding : ' + title_element_text)
    #     i += 1



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

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) 

    url_past = "https://www.meetup.com/bangkok-runners/events/?type=past" 
    Site_login(driver, BKRM_LOGIN_PAGE,Username,Password)

    driver.get(url_past)
    # scroll_to_bottom(driver)

    Site_Extract_Cal_Event(driver,url_past)
    # scroll_to_bottom(driver)
    # scroll_to_bottom(driver)
    # scroll_to_bottom(driver)
    # Site_Extract_Cal_Event(driver,url_past)

    # driver.get("https://th.jobsdb.com/th/en/Search/FindJobs") 
    # driver.get("https://th.jobsdb.com/th/search-jobs/devops/1") o


    # SITE_URL_EXTRACT = "https://www.meetup.com/bangkok-runners/events/calendar/"
    # M_Year = 2024
    # M_Month = 1
    # Site_Extract_Cal_Event(driver, SITE_URL_EXTRACT, M_Year, M_Month )



    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    df.to_csv(DF_DATA_FILE, index=False)

    conn = sqlite3.connect(BKRM_DB)

    df.to_sql(BKRM_TABLE_NAME, conn, if_exists='append', index=False)
    pd.read_sql('select * from ' + BKRM_TABLE_NAME, conn)

    logger.debug('JDB: Completed')
    logger.debug('JDB: -----')
    logger.debug('JDB: END')

    
if __name__ == "__main__":
    main()
#
# Name: JDB-PY-DETAILS
#
# Description: Extract information from a job posting (URL)
# Example: 
#   URL: https://th.jobsdb.com/th/en/job/job-300003002885733
#   Jobs Title
#   Company
#   Location
#   Date Posted
#   Jobs Highlight
#   Jobs Decription
#   Additional information
#       Career Level
#       Qualification
#       Years of Experience
#       Job Type
#       Company Website
#       Jobs Function
#   Company information
#       Company Industry
#       Benefits and Others


from selenium import webdriver 
from selenium.webdriver.chrome.service import Service 
from webdriver_manager.chrome import ChromeDriverManager 
import logging
import os

MyUsername = "myemai@email.com"
MyPWD = "mypassword"

JDB_HOME_DIR = "/Users/gonzaguepatinier/Documents/GitHub/LINKEDIN/JDB/"
JDB_JOB_URL = "https://th.jobsdb.com/th/en/job/job-300003002885733"
JDB_LOGIN_PAGE_URL = "https://th.jobsdb.com/th/en/login/jobseekerlogin"
JDB_LOGGER = 'my_logger_JDB'
JDB_LOGGER_FILE = JDB_HOME_DIR + 'JDB_my_log_file.log'

def Init_Logging(logger_name: str, logger_file_name):
    global logger

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # logger.setLevel(logging.DEBUG)
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

def JDB_LOGIN(local_webdriver: webdriver, site_login_page: str):
                                                                
    local_webdriver.get(site_login_page)                                                                                              

    id_username = "c_JbSrP1LnItDap_El0"
    username = local_webdriver.find_element("id",id_username )                                                                                              
    username.send_keys(MyUsername)                                                                                             

    id_password = "c_JbSrP1LnItDap_Pd0"
    pword = local_webdriver.find_element("id",id_password)                                                                                                  
    pword.send_keys(MyPWD)                                                                                                                   

    id_button = "reg-login-button"
    local_webdriver.find_element("id",id_button).click()

    # End of Function

def JDB_Jobs_Details_Process(local_webdriver: webdriver, url: str):

    local_webdriver.get(url)

    xpath_job_title = "//div[@data-automation='detailsTitle']"
    div_element = local_webdriver.find_element("xpath",xpath_job_title)                                                                                                                        
    div_text = div_element.text 
    print("Jobs Title: ")
    print(div_text)


    div_element = local_webdriver.find_element("xpath","//div[@data-automation='job-details-job-highlights']")                                                                                                                        
    div_text = div_element.text 
    print("Jobs Detail: ")
    print(div_text)

    # div_element = driver.find_element("xpath","//div[@class='z1s6m00 _1hbhsw66y _1hbhsw673 _1hbhsw674']")                                                                                                                        
    # div_element = driver.find_element("xpath","//div[@class='z1s6m00 _5135ge0 _5135ge2']")                                                                                                                        
    div_element = local_webdriver.find_element("xpath","//div[@data-automation='jobDescription']")                                                                                                                        
    div_text = div_element.text 
    print ("Jobs Description: ")
    print(div_text)

def main():
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) 

    #
    # To be loaded frmo json file
    #

    Init_Logging(JDB_LOGGER, JDB_LOGGER_FILE)
    
    os.system('clear')
    os.chdir(JDB_HOME_DIR)
    # MyCMD = 'cd ' + JDB_HOME_DIR
    # os.system(MyCMD)
    os.system('pwd') 

    logger.debug('JDB (JOBS): Start')

    # 
    # Nor required to be logged in
    #

    # Main 

    JDB_Jobs_Details_Process(driver, JDB_JOB_URL)

    quit()


    #
    # To be removed
    #

    # # div_elements = driver.find_elements("xpath","//div[@class='z1s6m00._1hbhsw66e'] | //span[@class='z1s6m00._1hbhsw64u.y44q7i0.y44q7i1.y44q7i21._1d0g9qk4.y44q7i7']")                                                                                                                          

    # # div_text = div_elements.text 
    # # print(dev_text)

    # # for element in div_elements: 
    # #     element_text = element.text 
    # #    print(element_text) 

    # # div_element = driver.find_element("xpath","//div[@class='z1s6m00 _1hbhsw66e'] | //span[@class='z1s6m00 _1hbhsw64u y44q7i0 y44q7i1 y44q7i21 _1d0g9qk4 y44q7i7']")                                                                                                                          

    # print ("total number of jobs: ")
    # # Total Number of Job

    # div_element = driver.find_element("xpath","//div[@class='z1s6m00 _1hbhsw66e']/.//span[@class='z1s6m00 _1hbhsw64u y44q7i0 y44q7i1 y44q7i21 _1d0g9qk4 y44q7i7']")                                                                                                                        
    # div_text = div_element.text 
    # print(div_text)

    # # Job Titles

    # print ("jobs title: ")

    # div_elements = driver.find_elements("xpath","//div[@class='z1s6m00 l3gun70 l3gun74 l3gun72']/.//span[@class='z1s6m00']")                                                                                                                        
    # for element in div_elements: 
    #     element_text = element.text 
    #     print(element_text) 

    # print ("Company: ")

    # # div_elements2 = driver.find_elements("xpath","//div[@class='z1s6m00 _1hbhsw6bm']/.//span[@class='z1s6m00 _17dyj7u1 _1hbhsw64u _1hbhsw60 _1hbhsw6r']")                                                                                                                        
    # div_elements2 = driver.find_elements("xpath","//div[@class='z1s6m00 _1hbhsw6bm']/.//a[@data-automation='jobCardCompanyLink']")                                                                                                                        


    # for element2 in div_elements2: 
    #     element_text = element2.text 
    #     print(element_text) 


    # print("\nSalary: \n")

    # # Not working yet ...

    # # div_elements3 = driver.find_elements("xpath","//div[@class='z1s6m00']/.//span[@class='z1s6m00 _1hbhsw64u y44q7i0 y44q7i3 y44q7i21 y44q7ih']")                                                                                                                        

    # div_elements3 = driver.find_elements("xpath","span[@class='z1s6m00 _1hbhsw64u y44q7i0 y44q7i3 y44q7i21 y44q7ih']/.//span[not(@class='z1s6m00 _17dyj7u1 _1hbhsw64u _1hbhsw60 _1hbhsw6r')]")                                                                                                                        


    # for element3 in div_elements3: 
    #     element_text = element3.text 
    #     print(element_text) 

if __name__ == "__main__":
    main()
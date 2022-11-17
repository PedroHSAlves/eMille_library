from selenium import webdriver
import warnings
import time
from  _remove_CT import _remove_ct
import paths as path

warnings.filterwarnings("ignore",category=DeprecationWarning)

class eMille():
    def __init__(self, user_name = "",password = ""):
        """
        The eMille library is for adding and removing cylinder tags and cycle time tags.

        Warnings:
        * By defauld, if a user_name and/or a password are not enterd, the authentication.txt file will be consulted.
        """

        self._user_name = user_name
        self._password = password

        self._driver = webdriver.Chrome(path.chrome_path)

        #Initializes the chrome driver
        try:
            self._driver.get(path.login_url)
        except:
            self._driver.close()
            raise UserWarning("Error 401 - Unauthorized. Check if your internet has access to the Stellantis network")
        
        self.__login()

    def __login(self):
        #Get the user_name and/or password from .txt file
        if self._user_name == "":
            with open('dependencies/authentication.txt') as f:
                lines = f.readlines()
            self._user_name = lines[0]

        if self._password == "":
            with open('dependencies/authentication.txt') as f:
                lines = f.readlines()
            self._password = lines[1]

        #Enter login
        element = self._driver.find_element_by_id("userName")
        element.send_keys(self._user_name)

        #Enter password
        element = self._driver.find_element_by_id("password")
        element.send_keys(self._password)

        try:
            element = self._driver.find_element_by_class_name("MuiButton-label")
            element.click()
            time.sleep(7) #webssite response time
        except:
            self._driver.close()
            raise TypeError('invalid password')
    
    def remove_cycle_time_tags(self,coletor_name,mttq_topic,config_name,backup = True):

        _remove_ct(self._driver,coletor_name,mttq_topic,config_name,backup)


    def remove_cylinder_tags(self):
        pass
    def add_cycle_time_tags(self):
        pass
    def add_cylinder_tags_old_version(self):
        pass
    def add_cylinder_tags_new_version(self):
        pass


#Test area

eM = eMille()
eM.remove_cycle_time_tags(coletor_name= "", mttq_topic="",config_name="")

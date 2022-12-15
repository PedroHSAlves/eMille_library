from selenium import webdriver
import warnings
import time
from __remove_CT import remove_ct
from __add_CT import add_CT
import paths as path
import ctypes, sys

# Made by Pedro Henrique - GitHub page @Pedro-Alvess

warnings.filterwarnings("ignore",category=DeprecationWarning)



class eMille():
    def __init__(self, user_name = "",password = ""):
        """
        The eMille library is for adding and removing cylinder tags and cycle time tags.

        Warnings:
        * By defauld, if a user_name and/or a password are not enterd, authentication will be done with the automatic authentication file.

        --> To manipulate the automatic authentication file use the class methods:
        * new_default_login() To add new settings;
        * change_default_login() To change the preset parameters;
        * delete_default_login() Deletes the data from the standard file;
        * show_default_login() Displays the preset setting;
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
    
    @classmethod
    def show_default_login(cls):
        """
        Class method.\n
        Shows the user name and password, if any, located in the automatic authentication file.
        """
        with open(path.file_name) as f:
            data = f.readlines()
            
        if data == []:
            print("Empty File!")
        elif data[0] == "\n":
            print("There is no username in authentication file!")
        elif len(data) == 1:
            print("There is no password in authentication file!")
        else:
            print('\nUser name: ', data[0],end='')
            print('Password: ', data[1])
    
    @classmethod
    def new_default_login(cls,user_name: str,password: str):
        """
        Class method.\n
        Inserts new user name and password into the automatic authentication file.
        """
        data = []
        data.append(user_name + "\n")
        data.append(password)

        out = open(path.file_name,'w')
        out.writelines(data)
        out.close
    
    @classmethod
    def change_default_login(cls,user_name = "",password = ""):
        """
        Class method.\n
        Change the user name and/or password of the default automatic authentication file.
        """
        data = open(path.file_name).readlines()

        if data[0] == "\n" or len(data) == 1:
            raise TypeError("The authentication file has inconsistencies in the data. Try using the class method new_default_login()")
        if user_name != "":
            data[0] = user_name + '\n'

        if password != "":
            data[1] = password
        
        out = open(path.file_name,'w')
        out.writelines(data)
        out.close
    
    @classmethod
    def delete_default_password(cls):
        """
        Class method.\n
        Deletes all data from the default automatic authentication file.
        """
        out = open(path.file_name,'w')
        out.writelines("")
        out.close
    
    def __is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False   
    
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
    
    def remove_cycle_time_tags(self,coletor_name: str,config_name: str,mttq_topic: str,backup = True):
        """
        Removes cycle time tags.\n
        By default the registration backup is enabled.\n
        For safety, you must pass all three filter parameters for tag removal.
        """
        if coletor_name == "" or config_name == "":
            if self.__is_admin():
                remove_ct(self._driver,coletor_name,mttq_topic,config_name,backup)
            else:
                self._driver.close()
                print("\nThis removal is HIGH RISK, and requires administrator privileges...")
                print("Within 10 secondes you will be redirected to the credentials screen.")

                for count in range(9):
                    print(".")
                    time.sleep(1)

                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        else:
            remove_ct(self._driver,coletor_name,mttq_topic,config_name,backup)
        


    def remove_cylinder_tags(self):
        pass
    def add_cycle_time_tags(self):
        add_CT(self._driver)
    def add_cylinder_tags_old_version(self):
        pass
    def add_cylinder_tags_new_version(self):
        pass
    


#Test area

eM = eMille()
eM.add_cycle_time_tags()
eM = eMille()
eM.remove_cycle_time_tags(coletor_name= "BET_BIW_PORTAANTERIOR_PREP_281X1H",config_name="OperationCycle", mttq_topic="",backup=False)





from selenium import webdriver
import paths as path
import time
from warnings import warn

class _remove_ct():
    def __init__(self,driver : webdriver.Chrome,coletor_name,mttq_topic,config_name,backup):
        self._COLETOR_NAME = coletor_name
        self._MTTQ_TOPIC = mttq_topic
        self._CONFIG_NAME = config_name
        self._backup = backup
        self._driver = driver
        self._counter = 0
        self._quantity_tags = 0

        self._configuration_screen()
    
    def _configuration_screen(self):
        """
        Navigates to the configuration page and inserts the filters
        """
        try:
            self._driver.get(path.config_url)
            time.sleep(1) #website response time
        except:
            self._driver.close()
            raise ValueError('error 404 - Not Found. Check if the url of the configuration page is correct.')
        
        #Inserts the filters
        element = self._driver.find_element_by_id("collectorName")
        element.send_keys(self._COLETOR_NAME)

        element = self._driver.find_element_by_id("configName")
        element.send_keys(self._CONFIG_NAME)

        element = self._driver.find_element_by_id("mqttTopic")
        element.send_keys(self._MTTQ_TOPIC)

        element = self._driver.find_element_by_class_name("MuiButton-textPrimary")
        element.click()
        time.sleep(6) #website response time

        self._len_tags
    
    @property
    def _len_tags(self):
        """
        Returns the number of visible tags in the configuration page
        """
        element = self._driver.find_element_by_css_selector("td > button.MuiButtonBase-root.MuiIconButton-root")
        self._quantity_tags = len(element)

        print(f"\nThere are {self._quantity_tags} data to be excluded")
        print(f"Have already been excluded {self._counter}")

    def _main(self):
        while self._quantity_tags > 0:
            try:
                element = self._driver.find_element_by_css_selector("td > button.MuiButtonBase-root.MuiIconButton-root")
                element[0].click()
                time.sleep(2) #website response time

                if self._backup:
                    pass #recover data function
                else:
                    pass #remove element function
                
                self._counter += 1
                self._len_tags
            except:
                warn(f'Error expanding line information {self._counter}')
        
        self._len_tags

        #Redundancy in the system in case of communication failures between the systems
        if self._quantity_tags > 0:
            warn('It was necessary to activate the recursion functionality to delete all tags')
            self._main()
        
        print("Completed execution")
        time.sleep(2) #system shutdow time
        self._driver.close()
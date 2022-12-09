from selenium import webdriver
import paths as path
import time
from warnings import warn
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

class remove_ct():
    def __init__(self,driver : webdriver.Chrome,coletor_name,mttq_topic,config_name,backup):
        self._COLETOR_NAME = coletor_name
        self._MTTQ_TOPIC = mttq_topic
        self._CONFIG_NAME = config_name
        self._backup = backup
        self._driver = driver
        self._counter = 0
        self._quantity_tags = 0
        self._action = ActionChains(self._driver)
        self._table_values = [[],[],[]] # [column,value,ordered value]

        self.__configuration_screen()
    
    def __configuration_screen(self):
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
        time.sleep(5) #website response time

        self.__len_tags
        self.__main()
    
    @property
    def __len_tags(self):
        """
        Returns the number of visible tags in the configuration page
        """
        
        element = self._driver.find_elements_by_css_selector("td > button.MuiButtonBase-root.MuiIconButton-root")
        self._quantity_tags = len(element)

        # print(element, end="\n\n")
        # print(type(element))
        # print(len(element))
        print(f"\nThere are {self._quantity_tags} data to be excluded")
        print(f"Have already been excluded {self._counter}")

    def __main(self):
        """
        """

        while self._quantity_tags > 0:
            try:
                element = self._driver.find_element_by_css_selector("td > button.MuiButtonBase-root.MuiIconButton-root")
                self._action.move_to_element(element).click().perform()
                time.sleep(2) #website response time
            except:
                  warn(f'Error expanding line information {self._counter}')

            if self._backup:
                self.__recover_data()
            else:
                self.__remove_element()
            
            self._counter += 1
            self.__len_tags

        
        self.__len_tags

        #Redundancy in the system in case of communication failures between the systems
        if self._quantity_tags > 0:
            warn('It was necessary to activate the recursion functionality to delete all tags')
            self._main()
        
        print("Completed execution")
        time.sleep(2) #system shutdow time
        self._driver.close()
    
    def __remove_element(self):
        """
        remove the element
        """
        try:
            element = self._driver.find_element_by_xpath("/html/body/div[1]/div/main/div[2]/div/form/button")
            element = self._driver.find_element_by_class_name("button#button-edit") 
            self._action.move_to_element(element).click().perform()
            element[0].click()
            time.sleep(1) #website response time

            remove_button = self._driver.find_elements_by_css_selector("span.MuiTypography-root.MuiListItemText-primary.MuiTypography-body1.MuiTypography-displayBlock")
            self._action.move_to_element(remove_button[2]).click().perform()

            print("\n Item successfully removed")
        except:
            self._counter -= 1
            warn('Error removing item')
        
        time.sleep(1) #website response time

        element = self._driver.find_element_by_xpath("/html/body/div[1]/div/main/div[1]/p")
        self._action.move_to_element(element).click().perform()
        time.sleep(5) #website response time

    def __recover_data(self):
        try:
            self._df = pd.read_excel(path.excel_path)
        except:
           raise SyntaxError('It was not possible to save the collected data. Check if worksheet "recover_data.xmls" exists')


        index = 0
        counter = 1

        self._table_values[0].append('Node')
        self._table_values[0].append('Send')
        self._table_values[0].append('Coletor')
        
        self._table_values[1].append(self._driver.find_element_by_xpath("/html/body/div[1]/div/main/div[3]/div/div[2]/div/div/div/div/div/div/table/tbody/tr[1]/td[5]").get_attribute("value"))
        self._table_values[1].append(-1)
        self._table_values[1].append(self._COLETOR_NAME)

        for index in range(9):
            self._table_values[0].append(self._driver.find_element_by_xpath(f"/html/body/div[1]/div/main/div[3]/div/div[2]/div/div/div/div/div/div/table/tbody/tr[2]/td/div/div/div/div[2]/div/div/div/table/tbody/tr[{counter}]/td[1]").get_attribute("value"))

            if index < 2:
                self._table_values[1].append(self._driver.find_element_by_xpath(f"/html/body/div[1]/div/main/div[3]/div/div[2]/div/div/div/div/div/div/table/tbody/tr[2]/td/div/div/div/div[2]/div/div/div/table/tbody/tr[{counter}]/td[2]").get_attribute("value")) 
            else:
                self._table_values[1].append(self._driver.find_element_by_xpath(f"/html/body/div[1]/div/main/div[3]/div/div[2]/div/div/div/div/div/div/table/tbody/tr[2]/td/div/div/div/div[2]/div/div/div/table/tbody/tr[{counter}]/td[2]").get_attribute("value"))
            counter += 1

        self.__store_data()
        self.__remove_element()
    
    def __store_data(self):
        try:

            for column in self._table_values[0]:

                if column == self._df.columns[0]:
                    index = self._table_values[0].index(column)
                    self._table_values[2].append(self._table_values[1][index])

                elif column == self._df.columns[1]:
                    index = self._table_values[0].index(column)
                    self._table_values[2].append(self._table_values[1][index])

                elif column == self._df.columns[2]:
                    index = self._table_values[0].index(column)
                    self._table_values[2].append(self._table_values[1][index])

                elif column == self._df.columns[3]:
                    index = self._table_values[0].index(column)
                    self._table_values[2].append(self._table_values[1][index])

                elif column == self._df.columns[4]:
                    index = self._table_values[0].index(column)
                    self._table_values[2].append(self._table_values[1][index])

                elif column == self._df.columns[5]:
                    index = self._table_values[0].index(column)
                    self._table_values[2].append(self._table_values[1][index]) 

                elif column == self._df.columns[6]:
                    index = self._table_values[0].index(column)
                    self._table_values[2].append(self._table_values[1][index])  

                elif column == self._df.columns[7]:
                    index = self._table_values[0].index(column)
                    self._table_values[2].append(self._table_values[1][index])  

                elif column == self._df.columns[8]:
                    index = self._table_values[0].index(column)
                    self._table_values[2].append(self._table_values[1][index])  

                elif column == self._df.columns[9]:
                    index = self._table_values[0].index(column)
                    self._table_values[2].append(self._table_values[1][index])   

                elif column == self._df.columns[10]:
                    index = self._table_values[0].index(column)
                    self._table_values[2].append(self._table_values[1][index]) 

                elif column == self._df.columns[11]:
                    index = self._table_values[0].index(column)
                    self._table_values[2].append(self._table_values[1][index])                                                                                     

            self._df.loc[len(self._df)] = self._table_values[2]
            
            self._df.to_excel(path.excel_path, index = False)
        except:
            raise TypeError('It was not possible to save the collected data. check that the column names are correct')
            



import paths as path
import pandas as pd
from selenium.webdriver.support.ui import Select
import time
import os
from selenium import webdriver

class add_CT():
    def __init__(self, driver : webdriver.Chrome ):
        """
        """
        self._dirver = driver
        self._index = 0
        self._excel_path = path.excel_add_ct_path
        self._element_list = ['select_field_plantId','select_field_shopId','select_field_collector','select_field_collectType','node','predefinedFields[2].Line',
                    'predefinedFields[3].ST','predefinedFields[4].Maq','addressTagsFields[0].value','addressTagsFields[1].value',
                    'addressTagsFields[2].value','addressTagsFields[3].value','addressTagsFields[0].order']
        self._topic_list = ['Node','Line','ST','Maq','VAL','CIL','Trigger 1','P1','P2','P3','Order Trigger 1']
        self._registered_lines = 0
        self._start_time = 0

        try:
            self._df = pd.read_excel(self._excel_path)
        except:
            raise TypeError("Excel 'add_cycle_time' was not found, check the integrity of the file.")

        self.__creation_screen()
        self.__main()
    
    def __creation_screen(self):
        """
        Navigates to the creat tag page.
        """
        self._dirver.get(path.creat_url)
        time.sleep(0.5)

        self._start_time = time.time()
    
    def __len_excel(self):
        """
        Tells how many tags there are in the spreadsheet.
        """
        return len(self._df['IdColetor'])
    
    def __fills_in_fields(self):
        """
        Fill in all the required fields
        """
        count = 0
        for num in range(13):
            if num <= 3:
                try:
                    element = Select(self._dirver.find_element_by_id(self._element_list[num]))
                    if num != 2:
                        element.select_by_index(1)
                        time.sleep(0.5)
                    else:
                        element.select_by_value(str(self._df['IdColetor'][self._index]))
                        time.sleep(0.5)
                except:
                    self._driver.close()
                    print("Registration failed, the program will restart!")
                    os.system('python eMille.py')
            else:
                try:
                    element = self._dirver.find_element_by_id(self._element_list[num])
                    if num >= 8 and num != 12:
                        value = self._df[self._topic_list[count + 2]][self._index]
                        if str(value) != "nan":
                            element.send_keys(value)
                    elif num == 12:
                        element.send_keys(10)
                    else:
                        element.send_keys(self._df[self._topic_list[count]][self._index])
                    count += 1
                except:
                    self._dirver.close()
                    print("Registration failed, the program will restart!")
                    os.system('python eMille.py')
        element.send_keys('\ue007') # Enter button code

    def __save_excel(self):
        """
        Save the data into excel.
        """
        excel_writer = pd.ExcelWriter(path.excel_add_ct_path)
        self._df.to_excel(excel_writer, index = False)
        excel_writer.save()

    def __show_registered_lines(self):

        self._registered_lines = len(self._df[self._df['Send'] == 1])
        print("\nRegistered lines: ", self._registered_lines)

        lines_to_be_registered = self.__len_excel() - self._registered_lines # Contar menos os sends
        print("Registration is missing: ", lines_to_be_registered, end="\n\n")

        end_time = time.time() - self._start_time
        expected_time = (lines_to_be_registered * end_time)/60
        print(f"Expected time to finish work: {expected_time:.2f} min")
        print(f"Last time set information: {end_time:.2f}")




    def __main(self):
        for line in range(self.__len_excel()):
            if self._df['Send'][self._index]:    
                self.__fills_in_fields()

                self._df['Send'][self._index] = 1

                self.__save_excel()
                self.__show_registered_lines()          
                self.__creation_screen() # F5 in page
            self._index += 1
        
        print("\nRegistered Data\n")

                


            


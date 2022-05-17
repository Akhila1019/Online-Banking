from selenium import webdriver  
import time  
from selenium.webdriver.common.keys import Keys  
print("sample test case started")  
driver = webdriver.Chrome("C:\\Users\\K M Yogitha\\Downloads\\chromedriver.exe")  
#driver=webdriver.firefox()  
#driver=webdriver.ie()  
#maximize the window size  
driver.maximize_window()  
#navigate to the url  
driver.get("http://127.0.0.1:5000//forgot_pwd")  
#identify the Google search text box and enter the value  
driver.find_element_by_name("accno").send_keys("123456")  #id/name
time.sleep(1)
driver.find_element_by_name("phone").send_keys("9886164791")  #id/name
time.sleep(3)  
#click on the Google search button  
driver.find_element_by_name("submit").send_keys(Keys.ENTER)  
time.sleep(3)  
#close the browser  
driver.close()  
print("sample test case successfully completed")
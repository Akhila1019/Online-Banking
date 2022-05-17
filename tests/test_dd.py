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
driver.get("http://127.0.0.1:5000/ddreq")  
#identify the Google search text box and enter the value  
driver.find_element_by_name("ano").send_keys("12345679")  #id/name
#click on the Google search button  
driver.find_element_by_name("bname").send_keys("yog")  #id/name
time.sleep(1)
driver.find_element_by_name("amou").send_keys("12340")  #id/name   
time.sleep(1)
driver.find_element_by_name("place").send_keys("ongole")  #id/name
time.sleep(1)
driver.find_element_by_name("submit").send_keys(Keys.ENTER)  
time.sleep(3)  
#close the browser  
driver.close()  
print("sample test case successfully completed")
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#unittest is a package for testing in python
#this is by deafult included in python
import unittest
import time

class QueryTest(unittest.TestCase):

    def setUp(self):
        # this method is going to be automatically executed
        # before the tests start
        PATH="./chromedriver"
        self.driver = webdriver.Chrome(PATH)

    def test_query_in_url(self):
        driver = self.driver
        driver.get("http://52.55.88.207:5000/query?q=home%20office")
        time.sleep(5)
        #we are waiting for the youtube search to finish
        result_list = driver.find_elements_by_class_name("youtube-video")
        self.assertEqual(len(result_list), 50)
        self.assertIn("home office", result_list[0].get_attribute('innerHTML'))

        #### test the search bar
        search_box = driver.find_element_by_name("description_search")
        search_box.send_keys("desk")
        search_button =driver.find_element_by_name("search_button")
        search_button.click()
        time.sleep(1)
        result_list = driver.find_elements_by_class_name("youtube-video")
        self.assertGreaterEqual(len(result_list), 1)
        self.assertIn("desk", result_list[0].get_attribute('innerHTML'))

if __name__ == "__main__":
    unittest.main()
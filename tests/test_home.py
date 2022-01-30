from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#unittest is a package for testing in python
#this is by deafult included in python
import unittest
import time

class HomeTest(unittest.TestCase):

    #override method: setup
    def setUp(self):
        #this method is going to be automatically executed
        #before the tests start
        PATH="./chromedriver"
        self.driver = webdriver.Chrome(PATH)

    def test_title(self):
        self.driver.get("http://52.55.88.207:5000/")
        self.assertIn("", self.driver.title)

    def test_link(self):
        self.driver.get("http://52.55.88.207:5000/")
        link = self.driver.find_element_by_link_text("link")
        link.send_keys(Keys.RETURN)
        self.assertIn("Query", self.driver.page_source)
        self.assertIn("no search results", self.driver.page_source)

if __name__ == "__main__":
    unittest.main()
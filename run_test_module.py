from __future__ import print_function
from testlink import TestlinkAPIClient, TestLinkHelper, TestGenReporter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re


class AppDynamicsJob( unittest.TestCase ):
    def setUp(self):
        self.driver = webdriver.Chrome("/mnt/d/myenv/testlink/src/drivers/chromedriver.exe")
        self.driver.implicitly_wait( 30 )
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_app_dynamics_job(self):
        driver = self.driver
        driver.set_page_load_timeout(10)
        driver.maximize_window()
        driver.get("https://www.x-kom.pl/")

        driver.find_element_by_xpath('//*[@id="navigation"]/ul/li[2]/a').send_keys(Keys.ENTER)
        driver.find_element_by_xpath(
            '//*[@id="pageWrapper"]/div[3]/div[2]/aside/section/ul/li[2]/ul/li[2]/a').send_keys(Keys.ENTER)

        product_price = driver.find_element_by_xpath(
            "//*[@id='productList']//*[@class='product-item product-impression']//*[@class='price-wrapper']//*[@class='prices']//*[@class='price text-nowrap']").text

        driver.find_element_by_xpath('//*[@id="productList"]/div[1]/button').send_keys(Keys.ENTER)

        driver.refresh()

        price_in_basket = driver.find_element_by_xpath(
            "//*[@id='basketItemsWrapper']//*[@class='basket-summary']//*[@class='total-basket-price pull-right']//*[@class='price-value-label js-basket-price']").text

        print('Cena produktu: ', product_price)
        print('Cena produktu w koszyku: ', price_in_basket)

        TESTLINK_API_PYTHON_SERVER_URL = 'http://localhost/testlink/lib/api/xmlrpc/v1/xmlrpc.php'
        TESTLINK_API_PYTHON_DEVKEY = '68eaccc81c42b4aaaba9fb973f6cec70'
        tl_helper = TestLinkHelper( TESTLINK_API_PYTHON_SERVER_URL, TESTLINK_API_PYTHON_DEVKEY )
        myTestLink = tl_helper.connect( TestlinkAPIClient )
        print( myTestLink.connectionInfo() )
        print( myTestLink.countProjects() )
        tc_info = myTestLink.getTestCase( None, testcaseexternalid='DppTs-2' )
        print( tc_info )
        tc_info = myTestLink.getProjectTestPlans( '1' )
        print( tc_info )
        myTestLink.reportTCResult( None, 2, None, 'p', 'some notes', guess=True,
                                   testcaseexternalid='DppTs-2',
                                   platformname='NewPlatform',
                                   execduration=3.9, timestamp='2019-06-09 16:00',
                                   steps=[{'step_number': 1, 'result': 'p', 'notes': 'brak bledow'}
                                          ] )


    def is_element_present(self, how, what):
        try:
            self.driver.find_element( by=how, value=what )
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.assertEqual( [], self.verificationErrors )


if __name__ == "__main__":
    unittest.main()

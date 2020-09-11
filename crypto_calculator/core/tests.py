from django.test import TestCase
from pycoingecko import CoinGeckoAPI
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
import random

# Create your tests here.
from core import constants


class APITestCase(TestCase):
    """
    test case to check api connection
    """

    def setUp(self):
        self.api_client = CoinGeckoAPI()

    def test_dashboards(self):
        """
        TEST:
            request to dashboard endpoint
            check is response status code successful
            check is response context data contains ethereum detail data
            check is response USD exchange rate equal to exchange rate of api
        """
        response = self.client.get('/core/dashboard/')
        usd_price_in_api = self.api_client.get_price(constants.ETHEREUM, constants.USD)[constants.ETHEREUM][
            constants.USD]

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['etheriums_details'][0]['market_data']['current_price']['usd'])

        usd_price = response.context['etheriums_details'][0]['market_data']['current_price']['usd']
        self.assertEqual(usd_price, usd_price_in_api)


class DashboardSeleniumTestCase(StaticLiveServerTestCase):
    """
    Automated test client to check front-end functionality
        init selenium, get current usd price from api
        check absolute difference of current price from html and api is less than 1
        send random integer[1:10] to ethereum input
        check resulting calculation value
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(5)
        cls.api_client = CoinGeckoAPI()
        cls.usd_price_in_api = cls.api_client.get_price(constants.ETHEREUM, constants.USD)[constants.ETHEREUM][
            constants.USD]

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_calculate_form(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/core/dashboard/'))

        # parse USD exchange rate
        exchange_rate = self.selenium.find_element_by_name("exchange_rate")
        usd_price = exchange_rate.get_attribute('value')
        self.assertLessEqual(abs(float(usd_price) - self.usd_price_in_api), 1)

        # Simulate input selenium count
        ethereum_input = self.selenium.find_element_by_name("ethereum")
        ethereum_count = random.randint(1, 10)
        ethereum_input.send_keys(ethereum_count)

        # Check calculation
        raw_calculated_usd_price = self.selenium.find_element_by_name('result').get_attribute('value')
        calculated_usd_price = float(raw_calculated_usd_price[:-1].strip())
        self.assertEqual(calculated_usd_price, self.usd_price_in_api * ethereum_count)

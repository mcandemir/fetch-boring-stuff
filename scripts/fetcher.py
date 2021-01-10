import selenium
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
import json
from scripts.cubis import FetchCubis
from scripts.util import clear


class Fetcher:

    # prepare selenium and load config.json ----------------------------------------------------------------------------
    def __init__(self):
        print('Getting driver ready..')

        # prepare config
        with open('./config.json', 'rb') as f:
            self.config = json.load(f)
            # print(self.config)

        # prepare webdriver
        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--silent')
        options.add_argument('--log-level=3')
        self.driver = Chrome(chrome_options=options, executable_path='./webdriver/chromedriver.exe')
        print('++Done.')

    # fetcher menu -----------------------------------------------------------------------------------------------------
    def start(self):
        while True:
            clear()
            print('\n=======Fetcher Menu======')
            opt = input("=========================\n1-Cubis grades\n2-Exit\n\nopt: ")

            if opt == '1':
                cubis_fetcher = FetchCubis(driver=self.driver, config=self.config)
                cubis_fetcher.start()

            elif opt == '2':
                self.driver.close()
                exit()

# ----------------------------------------------------------------------------------------------------------------------


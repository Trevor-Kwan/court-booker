from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from time import sleep
from datetime import datetime, timedelta
import pause
from inputs import login_details_input, venue_court_input, date_input, hour_input, target_datetime


def chrome_driver():
    chromedriver_autoinstaller.install()
    return webdriver.Chrome()


class CourtBooker:
    def __init__(self, launch_minutes=5, idle_minutes=20):
        # assign relevant user inputs
        self.username, self.password = login_details_input()
        self.venue, self.court_num = venue_court_input()
        self.date = date_input()
        self.hour = hour_input()
        # assign time related attributes
        self.target_dt = target_datetime()
        self.launch_dt = self.target_dt - timedelta(minutes=launch_minutes)
        self.idle_minutes = idle_minutes
        # initialize WebDriver
        self.driver = chrome_driver()
        self.driver.implicitly_wait(2)
        self.wait = WebDriverWait(self.driver, 10)

    def launch_login_page(self):
        print("Ready to Launch.")
        pause.until(self.launch_dt)
        self.driver.get('https://www.sport.gov.mo/zh/')
        self.driver.maximize_window()
        self.driver.find_element(by='xpath',
                                 value='/html/body/div[1]/div[3]/div[1]/div[1]/div[1]/form/div[6]/a'
                                 ).click()

    def account_login(self):
        password_incorrect = True
        while password_incorrect:
            # locate login input boxes
            username_box = self.driver.find_element(by='id', value='username')
            password_box = self.driver.find_element(by='id', value='password')

            # enter login values
            username_box.send_keys(self.username)
            password_box.send_keys(self.password)

            # attempt login
            self.driver.find_element(by='xpath', value='/html/body/section/form/button').click()

            # check if login was successful
            try:
                self.driver.find_element(by='class name', value='login-error')
            except NoSuchElementException:
                password_incorrect = False
                print('Login Successful.')
            else:
                # ask for login inputs again if login attempt failed
                print('\nLogin Failure. Please Try Again.')
                self.username, self.password = login_details_input()

    def begin_booking(self):
        self.driver.get('https://booking-new.sport.gov.mo/zh/onlinepay/booking')
        if datetime.today() <= self.target_dt:
            print(f"Waiting Until {self.target_dt}")
            pause.until(self.target_dt)  # wait until booking begins
            self.driver.refresh()

    def page_one_steps(self):

        # select venue
        venue_xpath = '/html/body/div/div/div[3]/div[1]/form/div[1]/select'
        self.wait_new_page(venue_xpath)  # wait until dropdown is found
        self.select_dropdown(venue_xpath, self.venue)

        # select sport
        sport_xpath = '/html/body/div/div/div[3]/div[1]/form/div[2]/div/select'
        self.select_dropdown(sport_xpath, 'bb')

        # select court
        court_xpath = '/html/body/div/div/div[3]/div[1]/form/div[3]/select'
        self.select_dropdown(court_xpath, str(self.court_num))

        # select date
        date_xpath = '/html/body/div/div/div[3]/div[1]/form/div[4]/select'
        self.select_dropdown(date_xpath, self.date)

        # agree to term and condition
        self.driver.find_element(by='id', value='agree').click()

        # proceed to next page
        self.driver.find_element(by='xpath', value='/html/body/div/div/div[3]/div[1]/form/div[6]/div/button[2]').click()
        pop_up_xpath = '/html/body/div[2]/div/div[2]/div/div[2]/div[3]/button[2]'
        self.wait.until(ec.visibility_of_element_located((By.XPATH, pop_up_xpath)))
        self.driver.find_element(by='xpath', value=pop_up_xpath).click()

    def page_two_steps(self):
        # select booking hour
        hour_xpath = f'/html/body/div[1]/div/div[3]/div[1]/div[1]/div[4]/div/div[{self.hour}]/div'
        self.wait_new_page(hour_xpath)  # wait until object is found
        self.driver.find_element(by='xpath', value=hour_xpath).click()

        # proceed to next step
        button_xpath = '/html/body/div[1]/div/div[3]/div[1]/div[1]/div[5]/div[2]/button[1]'
        self.driver.find_element(by='xpath', value=button_xpath).click()

    def select_dropdown(self, xpath, value):
        for _ in range(100):
            try:
                sport_select = Select(self.driver.find_element(by='xpath', value=xpath))
                sport_select.select_by_value(value)
            except NotImplementedError:
                sleep(0.01)
            else:
                break

    def driver_idle(self):
        print(f'Closing in {self.idle_minutes} Minutes.')
        pause.until(datetime.today() + timedelta(minutes=self.idle_minutes))

    def wait_new_page(self, xpath):
        try:
            self.wait.until(ec.visibility_of_element_located((By.XPATH, xpath)))  # wait until pop up is found
        except TimeoutException:
            print("Failed. Loading Too Long.")
            exit()


def main():
    court_booker = CourtBooker()
    court_booker.launch_login_page()
    court_booker.account_login()
    court_booker.begin_booking()
    court_booker.page_one_steps()
    court_booker.page_two_steps()
    court_booker.driver_idle()


if __name__ == '__main__':
    main()

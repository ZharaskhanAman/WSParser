from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import WebDriverException

class Parser:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        try:
            self.driver = webdriver.Chrome('chromedriver')
        except WebDriverException as e:
            raise Exception('*** Please install chromedriver first ***')
        self.driver.set_window_size(1024, 768)

    def login(self):
        self.driver.get("https://wsp.kbtu.kz/AttestationView")
        # Give the javascript time to render
        self.driver.implicitly_wait(5)
        time.sleep(6)

        # fill password
        password_field = self.driver.find_element_by_xpath("//input[@type='password']")
        password_field.send_keys(self.password)

        # fill username
        username_field = self.driver.find_element_by_xpath("//input[@type='text']")
        username_field.send_keys(self.username)

        # submit
        submit_button = self.driver.find_element_by_class_name("v-button-primary")
        submit_button.click()

    def get_schedule(self, year, semester):
        self.driver.get("https://wsp.kbtu.kz/StudentSchedule")
        # Give the javascript time to render
        self.driver.implicitly_wait(2)
        time.sleep(2)

        year_field = self.driver.find_elements_by_xpath("//input[@class='v-filterselect-input']")[0]
        # year_field.clear() doesnt work
        for i in range(9):
            year_field.send_keys(Keys.BACK_SPACE)

        # trim last character to fill with help of autofill
        year_field.send_keys(year[:-1])
        year_field.send_keys(Keys.RETURN)
        year_field.send_keys(Keys.RETURN)
        time.sleep(2)

        semester_field = self.driver.find_elements_by_xpath("//input[@class='v-filterselect-input']")[1]
        # year_field.clear() doesnt work
        for i in range(9):
            semester_field.send_keys(Keys.BACK_SPACE)

        # trim last character to fill with help of autofill
        semester_field.send_keys(semester[:-1])
        semester_field.send_keys(Keys.RETURN)

        self.driver.implicitly_wait(2)
        time.sleep(2)

        soup = BeautifulSoup(self.driver.page_source)

        days = soup.findAll("div", {"class": "v-slot v-slot-v-border-left-1-bfbfbf"})

        res = {}

        for day in days:
            day_label = day.find("div", {"class": "v-label v-widget bold v-label-bold v-label-undef-w"})
            if day_label is None:
                continue

            #print(day_label.text)
            lessons_array = []

            for lessons in day.findAll("div", {"class": "v-label v-widget v-margin-left-2 v-label-v-margin-left-2 v-margin-right-2 v-label-v-margin-right-2 v-align-center v-label-v-align-center v-has-width"}):
                print(lessons.text)
                # In format Языки программирования Иванов И.И. П 321 (13:00-14:00)
                text = lessons.text
                text = text.replace('\n', ' ')
                lessons_array.append(text)

            res[day_label.text] = lessons_array

        return res


if __name__ == '__main__':
    # credentials here:
    test = Parser("login", "password")
    test.login()
    time.sleep(6)
    test.get_schedule("2018-2019", "Весенний")

# driver.quit()

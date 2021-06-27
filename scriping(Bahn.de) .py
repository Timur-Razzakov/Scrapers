from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ES
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import sys

PATH = 'C:\Program Files (x86)\chromedriver.exe'


def main_scraping_part(
        origin_: str,
        destination_: str,
        date_to: str,
        date_from):
    global input_section
    _options = Options()
    _options.add_argument('--headless')
    driver = webdriver.Chrome(PATH, )

    '''
        Self-made generic func
    '''

    def Wait(time, what_by, second_param):
        return WebDriverWait(driver, time).until(
            ES.presence_of_element_located((what_by, second_param))
        )

    driver.get('https://www.bahn.de/')  # Get the page !

    '''
    Locate Fields

    '''
    origin = driver.find_element_by_xpath('//*[@id="js-auskunft-autocomplete-from"]')
    destination = driver.find_element_by_xpath('//*[@id="js-auskunft-autocomplete-to"]')
    date = driver.find_elements_by_xpath('//*[@class="center-inline hasDatepicker"]')
    start_date_field = date[0]
    end_date_field = date[1]
    submit_button = driver.find_element_by_xpath('//*[@class="btn pull-right js-submit-btn"]')

    """used to enter more information, to add (end_date_field)"""

    show_more = Wait(2, By.XPATH, '//*[@id="sectionQF"]/ul/li[1]')
    show_more.click()

    '''
        Feeding elements with DATA !
    '''
    start_date_field.clear()
    start_date_field.send_keys(date_to)

    origin.clear()
    origin.send_keys(origin_)

    '''
    Wait for promts to appear
    '''
    try:
        hit_city = Wait(4, By.XPATH, f'//span[contains(text(), "{origin_}")]')
        hit_city.click()
    except Exception:
        print('Hint not found or City does not exist in their DB1')
        sys.exit()

    ''' Click and clear the default values '''

    # end_date_field.click()
    # end_date_field.clear()
    # end_date_field.send_keys(date_from)
    # end_date_field.send_keys(Keys.RETURN)

    destination.send_keys(destination_)
    ''' Wait for promts to appear '''
    try:
        hit_city = Wait(4, By.XPATH, f'//span[contains(text(), "{destination_}")]')
        hit_city.click()
    except Exception:
        print('Hint not found or City does not exist in their DB2')
        sys.exit()

    submit_button.click()

    '''
         Check whether there is any data available
     '''
    try:
        all_items = Wait(10, By.XPATH, '//*[@id="resultsOverview"]')
    except Exception:
        print('result is EMPTY')

    all_items = driver.find_elements_by_xpath('//*[(@class = "boxShadow  scheduledCon ")]')

    """
    scroll
    """

    while True:
        # Scroll down to bottom
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight/1.5);")
        # Wait to load page
        try:
            progress_bar = WebDriverWait(driver, 3).until(
                ES.presence_of_element_located((By.XPATH,  '//*[@id="resultsOverviewLinksBottom"]/tr/td[2]/a'))
            )
            progress_bar.click()
        except :
            break


    all_items = driver.find_elements_by_xpath('//*[@id="resultsOverview"]')
    display(all_items, origin, destination, date)

'''
    Display the info u got
'''
def display(
    all_items: str,
    origin: str,
    destination: str,
    date: str) -> None:

    for item in all_items:
        price = item.find_element_by_xpath('//span[@class = "fareOutput"]').get_attribute('innerText')
        departure_time_info_wrapper = item.find_element_by_xpath('//td[@class = "station first "]')
        departure_time_info = departure_time_info_wrapper.find_element_by_xpath('//tr/td[contains(@class,"time")]').get_attribute('innerText')
        arrival_time_info_wrapper = item.find_element_by_class_name('station stationDest ')
        arrival_time_info = arrival_time_info_wrapper.find_element_by_class_name('time').get_attribute('innerText')

        print(price,departure_time_info,arrival_time_info)


'''
    Very important to have an entry point.
'''


def entry(
        city_from: str,
        city_to: str,
        date: str,
        date2: str) -> None:
    start_t = time.time()
    main_scraping_part(city_from, city_to, date, date2)
    print(f'Time taken => {time.time() - start_t}')



if __name__ == '__main__':
    entry('Nürnberg Hbf', 'Neumünster', '22.01.2021', '29.01.2021')

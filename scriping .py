from pyppeteer import launch
import asyncio
import logging
import time
import sys

async def main_scraping_part(
        origin_: str,
        destination_: str,
        date_to):
    start_t = time.time()
    global all_items, time
    logger = logging.getLogger('Scrape App')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('../scrape.log')
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s,%(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)


    browser = await launch(headless=False, autoClose=False)  # open brouser  it's demon
    page = await browser.newPage()  # открывает вкладку
    await page.goto('https://www.bahn.de/', timeout=50000)
    '''
        Feeding elements with DATA !
    '''
    date = await page.waitForXPath(' //*[@id="js-tab-auskunft"]/div/form/fieldset[1]/div[2]/div[1]/input',
                                   {'visable': True, 'timeout': 50000})
    await date.click({'clickCount': 3})
    await date.type(date_to)

    '''
    Locate Fields
    '''
    await page.waitForXPath('//*[@id="js-auskunft-autocomplete-from"]', {'visible': True, 'timeout': 50000})
    await page.click('[id=js-auskunft-autocomplete-from]', {'clickCount': 2})
    await page.type('[id=js-auskunft-autocomplete-from]', origin_)
    '''
    Wait for promts to appear
    '''
    departure_choice = await page.waitForXPath(f'//span[contains(text(), "{origin_}")]',
                                               {'visible': True, 'timeout': 50000})
    try:
        await departure_choice.click()
    except Exception:
        logger.info('Departure City InValid')
        sys.exit('Departure City InValid')
    '''
    Locate Fields
    '''
    await page.click('[id=js-auskunft-autocomplete-to]', {'clickCount': 1})
    await page.type('[id=js-auskunft-autocomplete-to]', destination_)
    await page.keyboard.press('Enter') # жмём интер вместо кнопки 'поиска'
    '''
    Wait for promts to appear
    '''
    # arrival_choice = await page.waitForXPath(f'//span[contains(text(), "{destination_}")]',
    #                                          {'visible': True, 'timeout': 5000})
    # try:
    #     await arrival_choice.click()
    # except Exception:
    #     logger.info('Arrival City Is Not Valid')
    #     sys.exit('Arrival City Is Not Valid')
    # # находим кнопку для вывода всех рейсов и кликаем по ней, пока не выйдут все
    while True:
        try:
            find_later_button = await page.waitForXPath('//*[@class="buttonGreyBg later"]',{'visible': True, 'timeout': 50000})
            await find_later_button.click()
        except Exception:
            break
    # ищем все билеты
    await asyncio.wait([page.waitForXPath('//*[@id="resultsOverview"]', {'visible': True, 'timeout': 50000})])
    try:
        all_items = await page.xpath('//*[@class="boxShadow  scheduledCon "]')
    except Exception:
        print("Tickets not found")


    dep_times = list()
    arr_times = list()
    prices = list()
    for item in all_items:
        price = await item.querySelector('tbody.boxShadow  span.fareOutput')
        time = await  item.querySelectorAll('td.time')
        dep_time =time[0]
        # arr_time = await item.xpath()

        price_text = await page.evaluate('(element) => element.textContent', price)
        dep_time_text = await  page.evaluate('(element) => element.textContent',dep_time)
        # arr_time_text = await  page.evaluate('(element )=> element.textContent',arr_time)

        prices.append(price_text.strip())
        dep_times.append(dep_time_text.strip())
        # arr_times.append(arr_time_text.strip())

    for price, dep_time, arr_time in zip(prices, dep_times, arr_times):
        print(price, dep_time,arr_times)

    print(f'Time taken => {time.time() - start_t}')



asyncio.get_event_loop().run_until_complete(
    main_scraping_part('Neumünster', 'Nürnberg Hbf', '22.01.2021'))

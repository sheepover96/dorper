from selenium import webdriver
from selenium.webdriver.support.ui import Select

browser = webdriver.Firefox()

year_range = [year for year in range(1996, 2020)]
month_range = [month+1 for month in range(12)]

for year in year_range:
    for month in month_range:
        print(str(year) + str(month).zfill(2))
        target = str(year) + str(month).zfill(2)
        browser.get('http://www1.mbrace.or.jp/od2/K/{}/mday.html'.format(target))
        elements = browser.find_elements_by_name('MDAY')
        #find day radio buttons
        for element in elements:
            element.click()
            download_button = browser.find_element_by_xpath('/html/body/center/form/center/input')
            download_button.click()
        browser.close()

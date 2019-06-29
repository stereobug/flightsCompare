from selenium import webdriver
from datetime import datetime as d 
from datetime import timedelta as td 



url = 'https://www.google.co.uk/flights/#flt=GLA.r/m/02j9z.2019-07-16*r/m/02j9z.GLA.2019-07-19;c:GBP;e:1;ls:1w;sd:1;er:177207493.-258125000.716613478.698125000;t:e'
exe = 'D:\\I.T\\python\\APIs\\flightsCompare\\chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1200x600') # optional
driver = webdriver.Chrome(executable_path=exe, chrome_options = options)
driver.get(url)

# city = driver.find_element_by_css_selector('#flt-app > div.gws-flights__flex-column.gws-flights__flex-filler > main.gws-flights__flex-box.gws-flights__active-tab.gws-flights__flex-filler.gws-flights__explore > div.gws-flights__sidebar-container > div > div.z2dw3 > div.bYsx5e > div:nth-child(2) > div > ol > li:nth-child(1) > div > div.uKOpFp4SF2X__info-container.flt-body2 > div.uKOpFp4SF2X__card-header > h3')
# stops = driver.find_element_by_css_selector('#flt-app > div.gws-flights__flex-column.gws-flights__flex-filler > main.gws-flights__flex-box.gws-flights__active-tab.gws-flights__flex-filler.gws-flights__explore > div.gws-flights__sidebar-container > div > div.z2dw3 > div.bYsx5e > div:nth-child(2) > div > ol > li:nth-child(1) > div > div.uKOpFp4SF2X__info-container.flt-body2 > div.uKOpFp4SF2X__card-header > div > span.gws-flights__flex-shrink.gws-flights__ellipsize')
# duration = driver.find_element_by_css_selector('#flt-app > div.gws-flights__flex-column.gws-flights__flex-filler > main.gws-flights__flex-box.gws-flights__active-tab.gws-flights__flex-filler.gws-flights__explore > div.gws-flights__sidebar-container > div > div.z2dw3 > div.bYsx5e > div:nth-child(2) > div > ol > li:nth-child(1) > div > div.uKOpFp4SF2X__info-container.flt-body2 > div.uKOpFp4SF2X__card-header > div > span.uKOpFp4SF2X__duration')
# price = driver.find_element_by_css_selector('#flt-app > div.gws-flights__flex-column.gws-flights__flex-filler > main.gws-flights__flex-box.gws-flights__active-tab.gws-flights__flex-filler.gws-flights__explore > div.gws-flights__sidebar-container > div > div.z2dw3 > div.bYsx5e > div:nth-child(2) > div > ol > li:nth-child(1) > div > div.uKOpFp4SF2X__info-container.flt-body2 > div.uKOpFp4SF2X__price-container > div > span')


try:
    for x in range(1,20):
        print("Result", x)
        city = driver.find_element_by_css_selector('#flt-app > div.gws-flights__flex-column.gws-flights__flex-filler > main.gws-flights__flex-box.gws-flights__active-tab.gws-flights__flex-filler.gws-flights__explore > div.gws-flights__sidebar-container > div > div.z2dw3 > div.bYsx5e > div:nth-child(2) > div > ol > li:nth-child(' + str(x) + ') > div > div.uKOpFp4SF2X__info-container.flt-body2 > div.uKOpFp4SF2X__card-header > h3')
        price = driver.find_element_by_css_selector('#flt-app > div.gws-flights__flex-column.gws-flights__flex-filler > main.gws-flights__flex-box.gws-flights__active-tab.gws-flights__flex-filler.gws-flights__explore > div.gws-flights__sidebar-container > div > div.z2dw3 > div.bYsx5e > div:nth-child(2) > div > ol > li:nth-child(' + str(x) + ') > div > div.uKOpFp4SF2X__info-container.flt-body2 > div.uKOpFp4SF2X__price-container > div > span')
        stops = driver.find_element_by_css_selector('#flt-app > div.gws-flights__flex-column.gws-flights__flex-filler > main.gws-flights__flex-box.gws-flights__active-tab.gws-flights__flex-filler.gws-flights__explore > div.gws-flights__sidebar-container > div > div.z2dw3 > div.bYsx5e > div:nth-child(2) > div > ol > li:nth-child(' + str(x) + ') > div > div.uKOpFp4SF2X__info-container.flt-body2 > div.uKOpFp4SF2X__card-header > div > span.gws-flights__flex-shrink.gws-flights__ellipsize')
        print(city.text)
        print(stops.text)
        print(price.text)
        print()
except Exception as e:
    print(e)


# print(city.text)
# print(stops.text)
# print(duration.text)
# print(price.text)

print("All done!")
driver.quit()


from selenium import webdriver

my_url = 'https://www.google.co.uk/flights/#flt=GLA.r/m/02j9z.2019-07-15*r/m/02j9z.GLA.2019-07-19;c:GBP;e:1;ls:1w;sd:1;er:177207493.-258125000.716613478.698125000;t:e'
driver = webdriver.PhantomJS(executable_path='D:\\I.T\\python\\APIs\\flightsCompare\\phantomjs.exe')
driver.get(my_url)
# p_element = driver.find_element_by_id(id_='intro-text')
p_element = driver.find_element_by_css_selector('#flt-app > div.gws-flights__flex-column.gws-flights__flex-filler > main.gws-flights__flex-box.gws-flights__active-tab.gws-flights__flex-filler.gws-flights__explore > div.gws-flights__sidebar-container > div > div.z2dw3 > div.bYsx5e > div:nth-child(2) > div > ol > li:nth-child(1) > div > div.uKOpFp4SF2X__info-container.flt-body2 > div.uKOpFp4SF2X__price-container > div > span')
print(p_element.text)


# result:
# 'Yay! Supports javascript'
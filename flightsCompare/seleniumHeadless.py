from selenium import webdriver
from datetime import datetime as d 
from datetime import timedelta as td 
import argparse



parser = argparse.ArgumentParser(description='look for bargain flights')
parser.add_argument('-d', '--departuredate', metavar='', required=False, help="date of departure | yyyy-mm-dd | default is tomorrow's date")
parser.add_argument('-r', '--returnedate', metavar='', required=False, help="date of return | yyyy-mm-dd | default is 3 days from departure")
parser.add_argument('-i', '--interval', metavar='', type=int, required=False, help="number of days away | default is 3 days from departure")

group = parser.add_mutually_exclusive_group()
group.add_argument('-O', '--Oneway', action='store_true', help='one way flights' )
group.add_argument('-R', '--Return', action='store_true', help='return flights' )

args = parser.parse_args()


if args.departuredate:
    depart = d.strptime(args.departuredate, "%Y-%m-%d").date()
else:
    depart = d.now().date() + td(days=1)


# url manipulation for one way or return flights 

if args.Oneway:
    url = 'https://www.google.co.uk/flights/#flt=GLA.r/m/02j9z.' + str(depart) + ';c:GBP;e:1;ls:1w;sd:1;er:177207493.-258125000.716613478.698125000;t:e;tt:o'
elif args.Return: 
    if not args.returnedate:
        interval = 3
    elif args.interval:
        interval = args.interval
    
    interval = td(days=interval)
    Return = depart + interval
    url = 'https://www.google.co.uk/flights/#flt=GLA.r/m/02j9z.' + str(depart) + '*r/m/02j9z.GLA.' + str(Return) + ';c:GBP;e:1;ls:1w;sd:1;er:177207493.-258125000.716613478.698125000;t:e'




exe = 'D:\\I.T\\python\\APIs\\flightsCompare\\chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1200x600') # optional
driver = webdriver.Chrome(executable_path=exe, chrome_options = options)
driver.get(url)



try:
    for x in range(1,20):
        print()
        print("Result", x)
        city = driver.find_element_by_css_selector('#flt-app > div.gws-flights__flex-column.gws-flights__flex-filler > main.gws-flights__flex-box.gws-flights__active-tab.gws-flights__flex-filler.gws-flights__explore > div.gws-flights__sidebar-container > div > div.z2dw3 > div.bYsx5e > div:nth-child(2) > div > ol > li:nth-child(' + str(x) + ') > div > div.uKOpFp4SF2X__info-container.flt-body2 > div.uKOpFp4SF2X__card-header > h3')
        stops = driver.find_element_by_css_selector('#flt-app > div.gws-flights__flex-column.gws-flights__flex-filler > main.gws-flights__flex-box.gws-flights__active-tab.gws-flights__flex-filler.gws-flights__explore > div.gws-flights__sidebar-container > div > div.z2dw3 > div.bYsx5e > div:nth-child(2) > div > ol > li:nth-child(' + str(x) + ') > div > div.uKOpFp4SF2X__info-container.flt-body2 > div.uKOpFp4SF2X__card-header > div > span.gws-flights__flex-shrink.gws-flights__ellipsize')
        duration = driver.find_element_by_css_selector('#flt-app > div.gws-flights__flex-column.gws-flights__flex-filler > main.gws-flights__flex-box.gws-flights__active-tab.gws-flights__flex-filler.gws-flights__explore > div.gws-flights__sidebar-container > div > div.z2dw3 > div.bYsx5e > div:nth-child(2) > div > ol > li:nth-child(' + str(x) + ') > div > div.uKOpFp4SF2X__info-container.flt-body2 > div.uKOpFp4SF2X__card-header > div > span.uKOpFp4SF2X__duration')
        price = driver.find_element_by_css_selector('#flt-app > div.gws-flights__flex-column.gws-flights__flex-filler > main.gws-flights__flex-box.gws-flights__active-tab.gws-flights__flex-filler.gws-flights__explore > div.gws-flights__sidebar-container > div > div.z2dw3 > div.bYsx5e > div:nth-child(2) > div > ol > li:nth-child(' + str(x) + ') > div > div.uKOpFp4SF2X__info-container.flt-body2 > div.uKOpFp4SF2X__price-container > div > span')
        print(city.text)
        print(stops.text)
        print(duration.text)
        print(price.text)
except Exception as e:
    print(e)


# print(city.text)
# print(stops.text)
# print(duration.text)
# print(price.text)


print("")
print("All done!")
driver.quit()


from selenium import webdriver
from datetime import datetime as d 
from datetime import timedelta as td 
import argparse


parser = argparse.ArgumentParser(description='look for bargain flights')
parser.add_argument('-d', '--departuredate', metavar='', required=False, help="date of departure | yyyy-mm-dd | default is tomorrow's date")
parser.add_argument('-r', '--returnedate', metavar='', required=False, help="date of return | yyyy-mm-dd | default is 3 days from departure")
parser.add_argument('-i', '--interval', metavar='', type=int, required=False, help="number of days away | default is 3 days from departure")
parser.add_argument('-p', '--pricecap', metavar='', type=int, required=False, help="price in GBP to match euqal or cheaper| default is £50")
parser.add_argument('-c', '--citydeaprting', metavar='', required=False, help="city departing from | default is GLA (Glasgow)")

group = parser.add_mutually_exclusive_group()
group.add_argument('-O', '--Oneway', action='store_true', help='one way flights | default is one way' )
group.add_argument('-R', '--Return', action='store_true', help='return flights | default is one way' )

args = parser.parse_args()


if args.departuredate:
    depart = d.strptime(args.departuredate, "%Y-%m-%d").date()
else:
    depart = d.now().date() + td(days=1)


# url manipulation for one way or return flights, default one way
if agrs.citydeaprting:
    cityDeparting = args.citydeaprting
else:
    cityDeparting = "GLA"


oneWay = 'https://www.google.co.uk/flights/#flt=' + cityDeparting + '.r/m/02j9z.' + str(depart) + ';c:GBP;e:1;ls:1w;sd:1;er:177207493.-258125000.716613478.698125000;t:e;tt:o'
url = oneWay

if args.Return: 
    if not args.returnedate:
        interval = 3
    elif args.interval:
        interval = args.interval
    
    interval = td(days=interval)
    Return = depart + interval
    bothWays = 'https://www.google.co.uk/flights/#flt=' + cityDeparting + '.r/m/02j9z.' + str(depart) + '*r/m/02j9z.GLA.' + str(Return) + ';c:GBP;e:1;ls:1w;sd:1;er:177207493.-258125000.716613478.698125000;t:e'
    url = bothWays



# selenium for chrome stuff 

exe = 'D:\\I.T\\python\\APIs\\flightsCompare\\chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1200x600') # optional
driver = webdriver.Chrome(executable_path=exe, chrome_options = options)
driver.get(url)


# price cap

if args.pricecap:
    priceCap = args.pricecap
else:
    priceCap = 50


# set list of dicts

Results = []

try:
    for x in range(1,100):
        print()
        city = driver.find_element_by_css_selector('#flt-app > div.gws-flights__flex-column.gws-flights__flex-filler > main.gws-flights__flex-box.gws-flights__active-tab.gws-flights__flex-filler.gws-flights__explore > div.gws-flights__sidebar-container > div > div.z2dw3 > div.bYsx5e > div:nth-child(2) > div > ol > li:nth-child(' + str(x) + ') > div > div.uKOpFp4SF2X__info-container.flt-body2 > div.uKOpFp4SF2X__card-header > h3')
        stops = driver.find_element_by_css_selector('#flt-app > div.gws-flights__flex-column.gws-flights__flex-filler > main.gws-flights__flex-box.gws-flights__active-tab.gws-flights__flex-filler.gws-flights__explore > div.gws-flights__sidebar-container > div > div.z2dw3 > div.bYsx5e > div:nth-child(2) > div > ol > li:nth-child(' + str(x) + ') > div > div.uKOpFp4SF2X__info-container.flt-body2 > div.uKOpFp4SF2X__card-header > div > span.gws-flights__flex-shrink.gws-flights__ellipsize')
        duration = driver.find_element_by_css_selector('#flt-app > div.gws-flights__flex-column.gws-flights__flex-filler > main.gws-flights__flex-box.gws-flights__active-tab.gws-flights__flex-filler.gws-flights__explore > div.gws-flights__sidebar-container > div > div.z2dw3 > div.bYsx5e > div:nth-child(2) > div > ol > li:nth-child(' + str(x) + ') > div > div.uKOpFp4SF2X__info-container.flt-body2 > div.uKOpFp4SF2X__card-header > div > span.uKOpFp4SF2X__duration')
        price = driver.find_element_by_css_selector('#flt-app > div.gws-flights__flex-column.gws-flights__flex-filler > main.gws-flights__flex-box.gws-flights__active-tab.gws-flights__flex-filler.gws-flights__explore > div.gws-flights__sidebar-container > div > div.z2dw3 > div.bYsx5e > div:nth-child(2) > div > ol > li:nth-child(' + str(x) + ') > div > div.uKOpFp4SF2X__info-container.flt-body2 > div.uKOpFp4SF2X__price-container > div > span')
        price = price.text
        
        Result = {
        'city' : city.text,
        'stops' : stops.text,
        'duration' : duration.text,
        'price' : str(price),
        }

        if not price[1:].isdigit():
            raise Exception('Price was not given for {}'.format(city.text))
        elif int(price[1:]) > priceCap:
            pass
            # raise Exception('Price was greater than £{} for {}'.format(priceCap, city.text))
        else:
            # print(Result)
            Results.append(Result)
except Exception as e:
    print(e)


# kill the driver ASAP or end up with loads of instances from testing
driver.quit()


# sort the list

if len(Results) == 0:
    print('No results for £', priceCap, "or under.")
else:
    # sort dict item in list by price and print in order
    ResultsSort = sorted(Results , key=lambda elem: "%03d" % (int(elem['price'][1:])))
    # now add headers to first index on the list
    ResultsSort.insert(0, {
        'city' : 'city',
        'stops' : 'stops',
        'duration' : 'duration',
        'price' : 'price',
        })


##### email part #####


from tabulate import tabulate
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import getpass


me = "***EMAIL***"
password = getpass.getpass()
server = 'smtp.outlook.com'
port = 587
you = '***EMAIL***'
#you = '***EMAIL***'


text = """
Hello,

Flights outgoing from""" + cityDeparting + """ on """  + str(depart) + """:

{table}

Regards,

Me"""

html = """
<html><body><p>Hello, </p> 
<p>Flights outgoing from""" + cityDeparting + """ on """ str(depart) + """:</p>
{table}
<p>Regards,</p>
<p>Me</p>
</body></html>
"""

# Results is the list of dicts from selenium 
data = ResultsSort

text = text.format(table=tabulate(data, headers="firstrow", tablefmt="grid"))
html = html.format(table=tabulate(data, headers="firstrow", tablefmt="html"))


message = MIMEMultipart("alternative", None, [MIMEText(text), MIMEText(html,'html')])
message['Subject'] = "Flights"
message['From'] = me
message['To'] = you
server = smtplib.SMTP(server, port)
server.ehlo()
server.starttls()
server.login(me, password)
server.sendmail(me, you, message.as_string())
server.quit()


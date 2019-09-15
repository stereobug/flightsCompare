# -*- coding: utf-8 -*-

# selenium
from selenium import webdriver
from datetime import datetime as d 
from datetime import timedelta as td 
import os
from tabulate import tabulate
import argparse

# threads
from  itertools import cycle
from threading import Thread
from time import sleep
import sys

def init_options():
    parser = argparse.ArgumentParser(description='look for bargain flights')
    parser.add_argument('-d', '--departuredate', metavar='', required=False, help="date of departure | yyyy-mm-dd | default is tomorrow's date")
    parser.add_argument('-r', '--returnedate', metavar='', required=False, help="date of return | yyyy-mm-dd | default is 3 days from departure")
    parser.add_argument('-i', '--interval', metavar='', type=int, required=False, help="number of days away before return | default is 3 days from departure")
    parser.add_argument('-p', '--pricecap', metavar='', type=int, required=False, help="price in GBP to match euqal or cheaper| default is £50")
    parser.add_argument('-c', '--citydeaprting', metavar='', required=False, help="city departing from | default is GLA (Glasgow)")
    parser.add_argument('-n', '--numberofextradays', metavar='', type=int, required=False, help="number of extra days after specifed date, to report on | default is for the specfied date only")
    parser.add_argument('-l', '--links', required=False, action='store_true', help="specify if you want links to page returned | default is off")

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-O', '--Oneway', action='store_true', help='one way flights | default is one way' )
    group.add_argument('-R', '--Return', action='store_true', help='return flights | default is one way' )

    args = parser.parse_args()
    
    return args


def animate():
    
    for pic in cycle(['|', '/', '-', '\\']):
    # for x in range(100):
        if done:
            break
        sys.stdout.write('\rsearching ' + pic)
        # sys.stdout.write('\rsearching {} {}'.format((x * " "), '>>'))
        sys.stdout.flush()
        sleep(0.1)
    # sys.stdout.write('\rDone!\n     ')


def generateURL(args, depart, day):
    # if first time round set the date, else increment for each extra day

    if day > 0:
        depart = depart + td(days=1)
        # print(depart)

    # url manipulation for one way or return flights 

    if args.citydeaprting:
        cityDeparting = args.citydeaprting
    else:
        cityDeparting = "GLA"
    
    # URL structure DRY

    root = 'https://www.google.co.uk/flights/#flt='
    link = '.r/m/02j9z.'
    currencyAndCoordinates = ';c:GBP;e:1;ls:1w;sd:1;er:177207493.-258125000.716613478.698125000;t:e'

    oneWay = '{}{}{}{}{};tt:o'.format(root, cityDeparting, link, depart,currencyAndCoordinates )
    url = oneWay

    if args.Return: 
        if not args.returnedate:
            interval = 3
        elif args.interval:
            interval = args.interval
        
        interval = td(days=interval)
        Return = depart + interval
        bothWays = '{}{}{}{}*r/m/02j9z.GLA.{}{}'.format(root, cityDeparting, link, depart, Return, currencyAndCoordinates)
        url = bothWays
    else:
        Return = args.Return

    # price cap
    if args.pricecap:
        priceCap = args.pricecap
    else:
        priceCap = 50

    return url, priceCap, cityDeparting, depart, Return


def gather(url, priceCap, depart):

    # configure google chrome and launch

    exe = os.path.join(os.path.dirname(os.path.abspath( __file__ )), 'chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_experimental_option('excludeSwitches', ['enable-logging']) # suppress message
    options.add_argument('window-size=1200x600') # optional
    driver = webdriver.Chrome(executable_path=exe, options = options)
    driver.get(url)

    # build report

    Results = []

    try:
        for x in range(1,50):
            city = driver.find_element_by_css_selector('#flt-app > div.gws-flights__flex-column.gws-flights__flex-filler > main.gws-flights__flex-box.gws-flights__active-tab.gws-flights__flex-filler.gws-flights__explore > div.gws-flights__sidebar-container > div > div.z2dw3 > div.bYsx5e > div:nth-child(2) > div > ol > li:nth-child(' + str(x) + ') > div > div.uKOpFp4SF2X__info-container.flt-body2 > div.uKOpFp4SF2X__card-header > h3')
            stops = driver.find_element_by_css_selector('#flt-app > div.gws-flights__flex-column.gws-flights__flex-filler > main.gws-flights__flex-box.gws-flights__active-tab.gws-flights__flex-filler.gws-flights__explore > div.gws-flights__sidebar-container > div > div.z2dw3 > div.bYsx5e > div:nth-child(2) > div > ol > li:nth-child(' + str(x) + ') > div > div.uKOpFp4SF2X__info-container.flt-body2 > div.uKOpFp4SF2X__card-header > div > span.gws-flights__flex-shrink.gws-flights__ellipsize')
            duration = driver.find_element_by_css_selector('#flt-app > div.gws-flights__flex-column.gws-flights__flex-filler > main.gws-flights__flex-box.gws-flights__active-tab.gws-flights__flex-filler.gws-flights__explore > div.gws-flights__sidebar-container > div > div.z2dw3 > div.bYsx5e > div:nth-child(2) > div > ol > li:nth-child(' + str(x) + ') > div > div.uKOpFp4SF2X__info-container.flt-body2 > div.uKOpFp4SF2X__card-header > div > span.uKOpFp4SF2X__duration')
            price = driver.find_element_by_css_selector('#flt-app > div.gws-flights__flex-column.gws-flights__flex-filler > main.gws-flights__flex-box.gws-flights__active-tab.gws-flights__flex-filler.gws-flights__explore > div.gws-flights__sidebar-container > div > div.z2dw3 > div.bYsx5e > div:nth-child(2) > div > ol > li:nth-child(' + str(x) + ') > div > div.uKOpFp4SF2X__info-container.flt-body2 > div.uKOpFp4SF2X__price-container > div > span')
            price = price.text
            
            Result = {
            'date': depart,
            'city' : city.text,
            'stops' : stops.text,
            'duration' : duration.text,
            'price' : str(price),
            }

            if not price[1:].isdigit():
                pass
                # raise Exception('Price was not given for {}'.format(city.text))
            elif int(price[1:]) > priceCap:
                pass
                # raise Exception('Price was greater than £{} for {}'.format(priceCap, city.text))
            else:
                # print(Result)
                Results.append(Result)
    except Exception as e:
        # will need to redirect to error log
        # print(e)
        pass

    # kill the driver ASAP or end up with loads of instances from testing
    driver.quit()

    return Results


def report(Results, depart, priceCap, cityDeparting, Return, url, args):
    print("")

    if len(Results) == 0:
        print('No results for £{} or under on {}'.format(priceCap, depart.strftime('%d-%b-%Y')))
    else:
        # sort by price and print in order
        ResultsSort = sorted(Results , key=lambda elem: "%03d" % (int(elem['price'][1:])))
        # squeeze in some headers to the top of the list
        ResultsSort.insert(0, {
        'city' : 'city',
        'stops' : 'stops',
        'duration' : 'duration',
        'price' : 'price',
        })
        if Return:
            print('Flights outgoing from {} on {} for £{} or less, returning {}:'.format(cityDeparting, depart.strftime('%d-%b-%Y'), priceCap, Return.strftime('%d-%b-%Y')))
        else:
            print('Flights outgoing from {} on {} for £{} or less:'.format(cityDeparting, depart.strftime('%d-%b-%Y'), priceCap))
        print()
        print(tabulate(ResultsSort, tablefmt="orgtbl", headers="firstrow"))
        print()
    if args.links:
        print("link:", url)



if __name__ == "__main__":
    args = init_options()

    # work out how many times we have to generate URL and get report
    if args.numberofextradays:
        daysToRun = args.numberofextradays + 1
    else:
        daysToRun = 1
    for day in range(0, daysToRun):
        if day == 0:
            if args.departuredate:
                depart = d.strptime(args.departuredate, "%Y-%m-%d").date()
            else:
                depart = d.now().date() + td(days=1)
        # start animation while program runs
        done = False
        animation = Thread(target=animate)
        animation.start()
        # make url, get info and report
        (url, priceCap, cityDeparting, depart, Return) = generateURL(args, depart, day)
        Results = gather(url, priceCap, depart)
        done = True
        # sleep(1)
        report(Results, depart, priceCap, cityDeparting, Return, url, args)
    print("All done!")
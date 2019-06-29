from requests_html import HTMLSession

# https://pypi.org/project/requests-html/
# https://html.python-requests.org/


session = HTMLSession()
r = session.get('https://www.google.co.uk/flights/#flt=GLA.r/m/02j9z.2019-07-15*r/m/02j9z.GLA.2019-07-19;c:GBP;e:1;ls:1w;sd:1;t:e')
r.html.render()


from urllib2 import build_opener,HTTPCookieProcessor
from cookielib import CookieJar

cj=CookieJar()
opener=build_opener(HTTPCookieProcessor(cj))
page='https://accounts.google.com/ServiceLoginBoxAuth'
resp=opener.open(page).read()
print resp

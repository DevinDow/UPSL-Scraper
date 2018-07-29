from bs4 import BeautifulSoup
import requests


# File Contents
#url_page = "http://www.upslsoccer.com/schedule"
#content = requests.get(url_page).content

file = open('upsl/upsl.html', 'r')
content = file.read()
file.close()

#print content


# Beautiful Soup
soup = BeautifulSoup(content, "lxml")

print "Title = "
print soup.find_all("title")

#print "tr = "
#print soup.find_all("tr")

print "tables = "
tables = soup.find_all("table")
print tables
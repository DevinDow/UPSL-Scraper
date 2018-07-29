from bs4 import BeautifulSoup
import requests


# File Contents
#url_page = "http://www.upslsoccer.com/schedule"
#content = requests.get(url_page).content

file = open('upsl/a.html', 'r')
content = file.read()
file.close()

#print content


# Beautiful Soup
soup = BeautifulSoup(content, 'lxml')


# Table Rows
for tr in soup.table.find_all('tr'):
    print(tr.prettify())


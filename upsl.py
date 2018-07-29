from bs4 import BeautifulSoup
import re
import requests


# Input
#url_page = "http://www.upslsoccer.com/schedule"
#content = requests.get(url_page).content

input = open('upsl/upsl.html', 'r')
content = input.read()
input.close()

#print content


# Write Output File
output = open ('upsl/output.html', 'w')
output.write("<html>\n")
output.write("\t<body>\n")
output.write("\t\t<table>\n")


# Beautiful Soup
soup = BeautifulSoup(content, 'lxml')


# Table Rows
for tr in soup.table.find_all('tr'):
    tdVenue = tr.select('td.schedule_venueName')
    #print tdVenue
    if (len(tdVenue) > 0):
        #print tr.prettify()
        venueName = tdVenue[0].contents[0]
        if (re.match('Lake Forest', venueName)):
            #print venueName
            output.write(tr.prettify())
    

# Close Output File
output.write("\t\t</table>\n")
output.write("\t</body>\n")
output.write("</html>\n")
output.close()
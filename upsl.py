from bs4 import BeautifulSoup
import re
import requests
import boto3


# Constants
INPUT_FILE = 'upsl.html'
OUTPUT_FILE = 'output.html'
S3_BUCKET = 'upsl-devin'


# Input
#url_page = "http://www.upslsoccer.com/schedule"
#content = requests.get(url_page).content

input = open(INPUT_FILE, 'r')
content = input.read()
input.close()

#print content


# Write Output File
output = open (OUTPUT_FILE, 'w')
output.write("<html>\n")
output.write("\t<head><title>UPSL @ Lake Forest</title></head>\n")
output.write("\t<body>\n")
output.write("\t\t<table>\n")


# Beautiful Soup
soup = BeautifulSoup(content, 'lxml')


# Table Rows
count = 0
for tr in soup.table.find_all('tr'):
    #TODO: capture date <tr>
    tdVenue = tr.select('td.schedule_venueName')
    #print tdVenue
    if (len(tdVenue) > 0):
        #print tr.prettify()
        venueName = tdVenue[0].contents[0]
        if (re.match('Lake Forest', venueName)):
            #print venueName
            output.write(tr.prettify())
            count += 1
    
print("%d  rows collected" % (count))

# Close Output File
output.write("\t\t</table>\n")
output.write("\t</body>\n")
output.write("</html>\n")
output.close()


# Upload to S3
s3 = boto3.resource('s3')
bucket = s3.Bucket(S3_BUCKET)
bucket.upload_file(OUTPUT_FILE, 'index.html', ExtraArgs={'ACL':'public-read'})


from bs4 import BeautifulSoup
import re
import requests
import boto3


# Constants
#INPUT_FILE = 'upsl.html'
OUTPUT_FILE = 'index.html'
S3_BUCKET = 'upsl-devin'


# Input
url = "http://www.upslsoccer.com/schedule"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
respone = requests.get(url, headers=headers)
print("Response to GET %s = %s" % (url, respone))
content = respone.text

#input = open(INPUT_FILE, 'r')
#content = input.read()
#input.close()


# Write Output File
output = open (OUTPUT_FILE, 'w')
output.write("<html>\n")
output.write("\t<head><title>UPSL @ Lake Forest</title></head>\n")
output.write("\t<body>\n")
output.write("\t\t<table border='1'>\n")


# Beautiful Soup
soup = BeautifulSoup(content, 'lxml')


# Table Rows
rowsMatched = 0
rowsTotal = 0
trDate = None
for tr in soup.table.find_all('tr'):
    tdVenue = tr.select('td.schedule_venueName')
    #print tdVenue
    if (len(tdVenue) > 0):
        #print tr.prettify()
        rowsTotal += 1
        
        venueName = tdVenue[0].contents[0]
        if (re.match('Lake Forest', venueName)):
            #print venueName
            output.write(trDate.prettify())
            output.write(tr.prettify())
            rowsMatched += 1
    else:
        trDate = tr
    
print("%d rows read" % (rowsTotal))
print("%d rows matched" % (rowsMatched))


# Close Output File
output.write("\t\t</table>\n")
output.write("\t</body>\n")
output.write("</html>\n")
output.close()


# Upload to S3
s3 = boto3.resource('s3')
bucket = s3.Bucket(S3_BUCKET)
response = bucket.upload_file(OUTPUT_FILE, 'index.html', ExtraArgs={'ACL':'public-read'})
print("Response to S3 Upload = %s" % (respone))

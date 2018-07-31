from bs4 import BeautifulSoup
import re
import requests
import boto3


standings = {}


def scrapeSchedule():
    print("\n\n*** scrapeSchedule()")

    # Constants
    OUTPUT_FILE = 'index.html'
    S3_BUCKET = 'upsl-devin'
    
    
    # Input from web
    content = scrapeWeb("http://www.upslsoccer.com/schedule")

    # Beautiful Soup
    soup = BeautifulSoup(content, 'lxml')
    
    
    # Write Output File
    output = open (OUTPUT_FILE, 'w')
    output.write("<html>\n")
    output.write("\t<head>\n")
    for header in soup.head.contents:
        output.write(str(header.encode('utf-8')))
    output.write("\t</head>\n")
    output.write("\t<body>\n")
    output.write("\t\t<table border='1'>\n")
    
    
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
            
            # Add <tr> to output
            venueName = tdVenue[0].contents[0]
            if (re.match('Lake Forest', venueName)):
                #print venueName

                # Add team ranks
                tdTeamA = tr.select('td.schedule_team_A_name')
                divTeamA = tdTeamA[0].select('div.scheduleTeamName')[0]
                teamA = divTeamA.contents[0]
                divTeamA.append(" (%s)" % (standings[teamA]))

                tdTeamB = tr.select('td.schedule_team_B_name')
                divTeamB = tdTeamB[0].select('div.scheduleTeamName')[0]
                teamB = divTeamB.contents[0]
                divTeamB.append(" (%s)" % (standings[teamB]))

                #print("%s (%s) vs %s (%s)" % (teamA, standings[teamA], teamB, standings[teamB]))

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
    bucket.upload_file(OUTPUT_FILE, 'index.html', ExtraArgs={'ACL':'public-read'})
    print("\"%s\" uploaded to \"%s\"" % (OUTPUT_FILE, bucket.name))



def scrapeStandings():
    print("\n\n*** scrapeStandings()")
    
    # Input from web
    content = scrapeWeb("http://www.upslsoccer.com/standings")

    # Beautiful Soup
    soup = BeautifulSoup(content, 'lxml')

    # Table Rows
    rowsMatched = 0
    for table in soup.find_all('table'):
        for tr in table.find_all('tr'):
            #print tr.prettify()
            tdRank = tr.select('td.standingsRankL')
            #print tdRank
            tdTeam = tr.select('td.standingsTeamNameL')
            #print tdTeam

            if (len(tdRank) > 0 and len(tdTeam) > 0):
                rank = tdRank[0].contents[0]
                #print tdTeam[0].a.b
                team = tdTeam[0].a.b.contents[0]
                #print("%s - %s" % (rank, team))
                standings[team] = rank
                rowsMatched += 1

    print("%d rows matched" % (rowsMatched))



def scrapeWeb(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    respone = requests.get(url, headers=headers)
    print("Response to GET %s = %s" % (url, respone))
    return respone.text
    


def main():
    scrapeStandings()
    scrapeSchedule()
    

if __name__ == "__main__":
    main()
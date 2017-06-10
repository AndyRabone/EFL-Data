from bs4 import BeautifulSoup
import urllib2
import pandas as pd
from textblob import TextBlob

import urllib
import json
import os.path

# Insane amount of data in JSON in BBC page!!!
urllist = ["http://www.bbc.co.uk/sport/football/39605009",
            "http://www.bbc.co.uk/sport/football/39550095",
            "http://www.bbc.co.uk/sport/football/39523330",
            "http://www.bbc.co.uk/sport/football/39463661",
            "http://www.bbc.co.uk/sport/football/39389681",
            "http://www.bbc.co.uk/sport/football/39753979",
            "http://www.bbc.co.uk/sport/football/39676222"]

filename = 'json.json'

# url = "http://www.bbc.co.uk/sport/football/39753979"

for link in urllist:
    if os.path.isfile(filename) == True:
        os.remove(filename)
        open(filename, "w")
    else:
        open(filename, "w")
    url = link
    # print url

    f = urllib.urlopen(url) # open up the URL
    dump = f.read() # read it into variable 'dump'

    # Going to have to iterate through and chunk the json up, probably using these tags.
    trim_start = dump.index('{"meta":')
    dump = dump[trim_start:]
    trim_end = dump.index('); });</script>')
    dump = dump[:trim_end]

    # print dump

    # probably need to export this as a text file
    f = open(filename, "w")
    f.write(dump)
    f.close()

    with open(filename) as json_data:
        d = json.load(json_data)
        injurytime = d["body"]["event"]["minutesIntoAddedTime"]
        attendance = d["body"]["event"]["attendance"]
        hometeam = d["body"]["event"]["homeTeam"]["name"]["full"]
        awayteam = d["body"]["event"]["awayTeam"]["name"]["full"]
        ref = d["body"]["event"]["officials"] #This is an array...
        ref = dict(ref[0]) # Coverted to a list, containing a dictionary! Hack out dictionary...
        referee = ref["name"]["full"]
        kickoff = d["body"]["event"]["startTimeInUKHHMM"]
        date = d["body"]["event"]["formattedDateInUKTimeZone"]["YYYYMMDD"]
        print date, kickoff,hometeam, awayteam, injurytime, attendance, referee

    f.close()

"""
url = 'https://www.sportinglife.com/football/live/22718/commentary'
page = urllib2.urlopen(url).read()
soup = BeautifulSoup(page)

target = "/home/andy/Documents/MatchOutput.csv"
pdcolumns = ['Time', 'Detail', 'Event', 'Event Detail', 'Team', 'Player']
content = []

# Can we grab date, Home/Away side?

for event in soup.find_all('li', class_='event'):
    detail_tag = event.find('div', class_='detail-col')
    detail = detail_tag and ''.join(detail_tag.stripped_strings)
    time_tag = event.find('div', class_='time-col')
    time = time_tag and ''.join(time_tag.stripped_strings)
    # Insert logic to calculate added time
    zen = TextBlob(detail)

    # Look for master events (i.e. free kicks, corners etc.)
    if zen.word_counts['attempt'] > 0 and zen.word_counts['saved']:
        MasterEvent = 'Attempt'
        FirstBracketIndex = int(zen.index('('))
        SecondBracketIndex = int(zen.index(')'))
        EventDetail = 'Attempt Saved'
        Team = detail[(FirstBracketIndex+1):SecondBracketIndex]
        Player = detail[:FirstBracketIndex].strip().replace('Attempt saved. ','').strip()


    elif zen.word_counts['hits'] > 0 and zen.word_counts['bar'] > 0:
        MasterEvent = 'Attempt'
        FirstBracketIndex = int(zen.index('('))
        SecondBracketIndex = int(zen.index(')'))
        EventDetail = 'Hit Bar'
        Team = detail[(FirstBracketIndex+1):SecondBracketIndex]
        Player = detail[:FirstBracketIndex].strip()

    elif zen.word_counts['missed'] > 0:
        MasterEvent = 'Attempt'
        FirstBracketIndex = int(zen.index('('))
        SecondBracketIndex = int(zen.index(')'))
        EventDetail = 'Attempt Missed'
        Team = detail[(FirstBracketIndex+1):SecondBracketIndex]
        Player = detail[:FirstBracketIndex].replace('Attempt missed. ', '').strip()

    elif zen.word_counts['attempt'] > 0 and zen.word_counts['blocked'] > 0:
        MasterEvent = 'Attempt'
        FirstBracketIndex = int(zen.index('('))
        SecondBracketIndex = int(zen.index(')'))
        EventDetail = 'Attempt Blocked'
        Team = detail[(FirstBracketIndex+1):SecondBracketIndex]
        Player = detail[:FirstBracketIndex].replace('Attempt blocked. ', '').strip()

    elif zen.word_counts['hits'] > 0 and zen.word_counts['post'] > 0:
        MasterEvent = 'Attempt'
        FirstBracketIndex = int(zen.index('('))
        SecondBracketIndex = int(zen.index(')'))
        EventDetail = 'Hit Post'
        Team = ''
        Player = ''

    elif zen.word_counts['goal'] > 0:
        MasterEvent = 'Goal'
        FirstBracketIndex = int(zen.index('('))
        SecondBracketIndex = int(zen.index(')'))
        EventDetail = detail[(SecondBracketIndex +1):].strip()
        Team = detail[(FirstBracketIndex+1):SecondBracketIndex]
        Player = ''

    elif zen.word_counts['foul'] > 0:
        MasterEvent = 'Foul'
        FirstBracketIndex = int(zen.index('('))
        SecondBracketIndex = int(zen.index(')'))
        EventDetail = MasterEvent
        Team = detail[(FirstBracketIndex+1):SecondBracketIndex]
        Player = detail[:FirstBracketIndex].replace('Foul by ', '')

    elif zen.word_counts['free'] > 0 and zen.word_counts['kick'] > 0:
        MasterEvent = 'Free Kick'
        FirstBracketIndex = int(zen.index('('))
        SecondBracketIndex = int(zen.index(')'))
        EventDetail = detail[(SecondBracketIndex+1):].replace('wins a free kick in the ', '').strip()
        Team = detail[(FirstBracketIndex+1):SecondBracketIndex]
        Player = detail[:FirstBracketIndex]

    elif zen.word_counts['substitution'] > 0:
        MasterEvent = 'Substitution'
        PeriodIndex = int(detail.index('.'))
        EventDetail = detail[(PeriodIndex+1):].strip()
        Team = detail[:PeriodIndex].replace('Substitution, ', '').strip()
        Player = ''

    elif zen.word_counts['corner'] > 0:
        MasterEvent = 'Corner'
        PeriodIndex = int(detail.index('.'))
        Team = detail[:PeriodIndex].replace('Corner, ', '').strip()
        EventDetail = detail[(PeriodIndex +1):].strip()
        Player = ''

    elif zen.word_counts['yellow'] > 0 and zen.word_counts['card'] > 0:
        MasterEvent = 'Yellow Card'
        FirstBracketIndex = int(zen.index('('))
        SecondBracketIndex = int(zen.index(')'))
        EventDetail = 'Foul'
        Team = detail[(FirstBracketIndex+1):SecondBracketIndex]
        Player = detail[:FirstBracketIndex].strip()

    elif zen.word_counts['red'] > 0 and zen.word_counts['card'] > 0:
        MasterEvent = 'Red Card'
        EventDetail = ''
        Team = ''
        Player = ''

    elif zen.word_counts['second'] > 0 and zen.word_counts['half'] > 0 and zen.word_counts['ends'] > 0:
        MasterEvent = 'End of Game'
        EventDetail = ''
        Team = ''
        Player = ''

    else:
        MasterEvent = ''
        EventDetail = ''
        Team = ''
        Player = ''

    # Append events to list - skip over inconsequential events.
    if MasterEvent <> '':
        content.append([time[:-1], detail, MasterEvent, EventDetail.replace('.',''), Team, Player])

    # Dump list to dataframe
    df = pd.DataFrame.from_records(content, columns=pdcolumns)

# Output to csv
df.to_csv(target, sep=',', header=True)

#for row in df:
print df
"""



"""
Commentary analysis -

Secnd Half begins
First Half ends
Full time - 'Second Half Ends, {Home Team} #, {Away Team} #.

Attempt missed. {Player} ({Team}) {action} {location}
Attempt saved. {Player} ({Team}) {action} {location}
Attempt blocked. {Player} ({Team}) {action} from {location} is blocked.
{Player} ({team}) hits the bar with {action} from {location}
Goal! {HomeTeam} #, {AwayTeam} #. {Player} ({Team}) {action} to {location}.
Goal! {HomeTeam} #, {AwayTeam} #. {Player} ({Team}) {action} to {location}. Assisted by {Player}.

Corner, {Team}. Conceded by {Player}.

Foul by {Player} ({Team})
{Player} ({Team}) wins a free kick in the {defensive/attacking} half.
{Player} ({Team}) wins a free kick on the {right/left} wing.
{Player} ({Team}) is shown the yellow card.
{Player} ({Team}) is shown the yellow card for {offence}.

Substitution, {Team}. {Substitute On} replaces {Substitute Off}.
Substitution, {Team}. {Substitute On} replaces {Substitute Off} because of an injury.


"""
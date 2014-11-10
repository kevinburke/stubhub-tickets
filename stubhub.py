import csv
from datetime import datetime
from email import utils
import json
import pprint
import sys
import time

import requests

from requests_oauthlib import OAuth2Session

def get_data():
    with open('token_data.json') as f:
        token_data = json.load(f)

    stubhub = OAuth2Session(r'kev@inburke.com', token=token_data)

    r = stubhub.get('https://api.stubhub.com/search/catalog/events/v2', params={'q': 'Golden State Warriors', 'date': '2014-11-09T00:00 TO 2014-11-17T23:59'})
    print r.content
    r.raise_for_status()
    return r.json()

def dump_data(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_data_from_file(filename):
    with open(filename) as f:
        return json.load(f)

def get_event(events, teamname):
    for event in events:
        attributes = event['attributes']
        for attr in attributes:
            if attr['name'] == 'act_secondary' and attr['value'] == teamname:
                return event
    raise KeyError()

#d = load_data_from_file('warriors_events.json')
d = get_data()

event = get_event(d['events'], 'San Antonio Spurs')
print event['ticketInfo']
nowtimestamp = time.time()
foo = csv.writer(sys.stdout)
foo.writerow([utils.formatdate(nowtimestamp), event['ticketInfo']['totalListings'], event['ticketInfo']['minPrice']])

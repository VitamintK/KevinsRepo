"""for noun in dictionarynouns+frequentpropernouns:
    for article in ('','a','the'):
        count quantity of usages of 'thirsty for ' article noun in google books
        count quantity of usages of 'thirsty for ' article noun in google search
        same for hungry
    yield the 12 values"""

import json
import urllib

def showsome(searchfor):
  query = urllib.urlencode({'q': searchfor})
  url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
  search_response = urllib.urlopen(url)
  search_results = search_response.read()
  results = json.loads(search_results)
  data = results['responseData']
  print 'Total results: %s' % data['cursor']['estimatedResultCount']
  hits = data['results']
  print 'Top %d hits:' % len(hits)
  for h in hits: print ' ', h['url']
  print 'For more results, see %s' % data['cursor']['moreResultsUrl']

def estimatedresultcount(term):
  query = urllib.urlencode({'q': term})
  url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
  search_response = urllib.urlopen(url)
  search_results = search_response.read()
  results = json.loads(search_results)
  data = results['responseData']
  try:
    return data['cursor']['estimatedResultCount']
  except:
    return '0'

def hungerorthirst(*args):
  for term in args:
    hung=0
    for i in ('hunger','hungry'):
      searchfor = "'{0} for {1}'".format(i,term)
      rescount = estimatedresultcount(searchfor)
      hung+=int(rescount)
      print '%s: %s'%(searchfor,rescount)
    thirst=0
    for i in ('thirst','thirsty'):
      searchfor = "'{0} for {1}'".format(i,term)
      rescount = estimatedresultcount(searchfor)
      thirst+=int(rescount)
      print '%s: %s'%(searchfor,rescount)
    yield hung,thirst

def ui(*args):
  for i in hungerorthirst(*args):
    if i[0]>i[1]:
      yield -1
    elif i[1]>i[0]:
      yield 1
    else:
      yield 0


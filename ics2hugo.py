import argparse
import icalendar
import urllib2
import re
import codecs

def fetch_ics(url):
    ics = urllib2.urlopen(url)
    return ics.read()

def parse_ics(ics):
    items = []
    cal = icalendar.Calendar.from_ical(ics)
    for comp in cal.walk():
        if comp.name == 'VEVENT':
            event = {}
            print comp.get('summary')
            event['title'] = u''.join(comp.get('summary')).encode('utf-8')
            event['date'] = str(comp.get('dtstart').dt)
            event['text'] = u''.join(comp.get('description')).encode('utf-8')
            items.append(event)
    return items

def write_hugo(path,items):
    for item in items:
        fname = item['title']
        fname = fname.replace(' ','-')
        fname = re.sub('[^0-9a-zA-Z-]*','',fname)
        fpath = path+'/'+fname+'.md'
        with open(fpath,'w') as mdfile:
            mdfile.write('+++\n')
            mdfile.write('date = \"'+item['date']+'\"\n')
            mdfile.write('title = \"'+item['title']+'\"\n')
            mdfile.write('+++\n\n')
            mdfile.write(item['text'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ics2hugo (markdown) conversion tool.')
    parser.add_argument('--url', required=True, help='url to ics calendar.')
    parser.add_argument('--path', required=True ,help='output path of markdown files.')
    args = parser.parse_args()
    ics = fetch_ics(args.url)
    items = parse_ics(ics)
    write_hugo(args.path,items)

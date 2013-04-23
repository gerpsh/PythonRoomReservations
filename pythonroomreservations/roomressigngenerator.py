import time
import json
import urllib2
from calendarevent import CalendarEvent
from roomrescalendar import RoomResCalendar

#specify start date and end date, this will need to be change before
#the signs are generated each week
start_date = '2013-04-08'
end_date = '2013-04-12'

#this string specifies the format that the output should be (jsonc, or compact json)
#the date range of the events to fetch from the calendar data
#and to order the output by start time in a ascending order
engine = 'https://www.google.com/calendar/feeds/'
caboose = ('prettyprint=true&alt=jsonc&start-min=' + start_date + 'T00:00:00&start-max=' + end_date + 'T23:59:59&orderby=starttime&sortorder=ascending')

#dictionary of the name of each room reservation calendar and the corresponding url used to fetch its data
#We use a read only version of the calendar data which can be fetched using a private 'magic cookie',
#which is a code provided by google that can be included in a url to request the data
#example: {'Room 1000 Reservation Calendar': (engine + '234gk54hj2lkh5nknvb34xfg@group.calendar.google.com/private-423hkjs8d7x98s7/full?' + caboose)}
#the 'full' at the end specifies that we want google to give us all calendar data
urls = {}


#goes through entry in the urls dictionary, fetches data, parses data,
#turns the data into an html document, and writes the document to a file
for room, url in urls.iteritems():
    url_file = open('url_file.txt', 'w')
    url_file.write(url + '\n')
    #initializes calendar object with title
    table = RoomResCalendar(room)
    #creates file for writing html
    html_file = open('Calendars\\' + room + '.html', 'w')
    #requests data from google using url in dictionary
    response = urllib2.urlopen(url)
    #parses data into json object so that we can more easily manipulate it
    calendar_data = json.load(response)
    #gets only the data we need from the returned data, which is the event data
    events_data = calendar_data['data']['items']
    #loops through list of events data, creates an event object from the data, 
    #and adds the event object to the RoomResCalendar object we made
    for event_datum in events_data:
        #Some events don't have some of the data we need
        #If it doesn't have a title, start time, and end time,
        #Then it's definitely not on the calendar for the week and
        #is probably a recurring event that showed up in our data
        #This block will try to get the data we want, and if there isn't data that we need,
        #it will throw an error
        #We handle the error by just moving onto the next event in the data
        try:
            event_title_data = event_datum['title']
            event_start_data = event_datum['when'][0]['start']
            event_end_data = event_datum['when'][0]['end']
            calendar_event = CalendarEvent(event_title_data, event_start_data, event_end_data)
            table.add_event(calendar_event)
        except:
            continue
    #Sorts the events within the table
    #Although the events should already be mostly sorted because of the way we constructed the url ('orderby=...',
    #recurring events seem the break the rules, so we still need to do our own sort
    table.sort_events()
    #write html document to file we opened
    html_file.write(table.to_html())
    #close file because we are done with it
    html_file.close()

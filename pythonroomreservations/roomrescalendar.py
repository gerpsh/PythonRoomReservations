from calendarevent import CalendarEvent
import time
import itertools

class RoomResCalendar:

    #properties
    #different lists for different days make spacing between
    #events on different days easier in html 
    def __init__(self, heading):
        self.heading = heading
        self.monday_events = []
        self.tuesday_events = []
        self.wednesday_events = []
        self.thursday_events = []
        self.friday_events = []
        self.saturday_events = []
        self.sunday_events = []
    
    #adds event to object, in appropriate day list
    def add_event(self, event):
        if event.day == 'Monday':
            self.monday_events.append(event)
        elif event.day == 'Tuesday':
            self.tuesday_events.append(event)
        elif event.day == 'Wednesday':
            self.wednesday_events.append(event)
        elif event.day == 'Thursday':
            self.thursday_events.append(event)
        elif event.day == 'Friday':
            self.friday_events.append(event)
        elif event.day == 'Saturday':
            self.saturday_events.append(event)
        elif event.day == 'Sunday':
            self.sunday_events.append(event)
        
        
    #sorts event objects within day lists based on their start_time property
    def sort_events(self):
        self.monday_events = sorted(self.monday_events, key=lambda event: event.start_time)
        self.tuesday_events = sorted(self.tuesday_events, key=lambda event: event.start_time)
        self.wednesday_events = sorted(self.wednesday_events, key=lambda event: event.start_time)
        self.thursday_events = sorted(self.thursday_events, key=lambda event: event.start_time)
        self.friday_events = sorted(self.friday_events, key=lambda event: event.start_time)
        self.saturday_events = sorted(self.saturday_events, key=lambda event: event.start_time)
        self.sunday_events = sorted(self.sunday_events, key=lambda event: event.start_time)
    
    #converts RoomResCalendar into string html representation of itself
    def to_html(self):
        #For some reason, a simple addition of lists of complext objects is not allowed
        #in python.  Just using '+' to concatenate the event lists turns them into
        #a list of lists. Here's a way that works, which uses itertools and list
        #casting
        all_events = list(itertools.chain(self.monday_events, self.tuesday_events,
                                           self.wednesday_events, self.thursday_events,
                                           self.friday_events, self.saturday_events,
                                           self.sunday_events))

        #this text can be inserted to represent a blank row in the table
        blank_row  = ('<tr>\n'
                      '\t<td>&nbsp;</td>\n'
                      '\t<td>&nbsp;</td>\n'
                      '\t<td>&nbsp;</td>\n'
                      '\t<td>&nbsp;</td>\n'
                      '\t<td>&nbsp;</td>\n'
                      '</tr>\n')

        #events on the table are grouped and separated by day if there is enough space on the table.
        #the separator will be a blank row
        #if there is room to skip, skip is set to True and gap is set to blank_row
        skip = False
        gap  = ''

        if len(all_events) < 12:
            gap = blank_row
            skip = True
        
        #adds blank rows to end of table to fill the rest of the page (if necessary)
        extra_rows = 0
        if skip:
            extra_rows = 12 - len(all_events)
        else:
            extra_rows = 16 - len(all_events)

        #adds all day lists to single list of lists to prepare for iteration
        all_days_lists = [self.monday_events, self.tuesday_events, self.wednesday_events,
                          self.thursday_events, self.friday_events, self.saturday_events, 
                          self.sunday_events]

        #initializes html document
        html_calendar = ('<html>\n'
                         '<title>' + self.heading + '</title>\n'
                         '<head>\n'
                         '<link rel="stylesheet" type="text/css" href="style.css">\n'
                         '</head>\n'
                         '<body>\n'
                         '<h1>' + self.heading + '</h1>\n'
                         '<table>\n'
                         '<tr>\n'
                         '\t<th>Day</th>\n'
                         '\t<th>Date</th>\n'
                         '\t<th>Time</th>\n'
                         '\t<th>Study</th>\n'
                         '\t<th>Contact</th>\n'
                         '</tr>\n')
        
        #loops through the list of event day lists, turning each event in the list into its html representation
        for event_list in  all_days_lists:
            #loops through day list events
            if len(event_list) > 0:
                for event in event_list:
                    #converts event start time into H:MM AM/PM format
                    short_start = time.strftime('%I:%M%p', event.start_time).lstrip('0')
                    #does the same for end time
                    short_end = time.strftime('%I:%M%p', event.end_time).lstrip('0')
                    #converts month of start time into number without leading zero if present
                    short_event_month = time.strftime('%m', event.start_time).lstrip('0')
                    #does the same for the day
                    short_event_day = time.strftime('%d', event.start_time).lstrip('0')
                    #convert year into 2-digit year
                    short_event_year = time.strftime('%y', event.start_time)
                    #puts these values together to make the final representation of the date
                    short_event_date = (short_event_month + '/' + short_event_day + '/' + short_event_year)
                    #yes, that whole block was annoying, but there isn't presently a better way to do it python using these data structures
                
                    #this makes the final representation of an event as a row on the table
                    html_calendar = html_calendar + ('<tr>\n'
                                                     '\t<td>' + event.day + '</td>\n'
                                                     '\t<td>' + short_event_date + '</td>\n'
                                                     '\t<td>' + short_start + '-' + short_end + '</td>\n'
                                                     '\t<td bgcolor = "' + event.color + '">' + event.study + '</td>\n'
                                                     '\t<td>' + event.contact + '</td>\n'
                                                     '</tr>\n')
        
            #if there is enough space on the page to group events by day, 'gap' will be a blank space.
            #if not, gap will have already been set to nothing, and there will be no actual gap)
                html_calendar = html_calendar + gap
    
        #if there is extra space on the page, extra rows will be printed to fill the page
        if (extra_rows > 0):
            for i in range(extra_rows):
                html_calendar = html_calendar + blank_row
    
        #complete html document
        html_calendar = html_calendar + ('</table>\n'
                                         '</body>\n'
                                         '</html>\n')

        #return string representation of table
        return html_calendar
    

    

        

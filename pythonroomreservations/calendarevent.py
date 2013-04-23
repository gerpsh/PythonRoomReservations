import time
import re



class CalendarEvent:

    #dictionary of contact associated with each study
    #dictionaries cannot have two of the same key (study letters)
    #e.g. {'GGG': 'John'}
    study_contacts  = {}

    #dictionary of highlight colors associated with each study
    #e.g. {'GGG': 'Green'}
    study_colors = {}

    #dictionary of day names associated with their number within the data
    week_days = {0: 'Monday', 
                 1: 'Tuesday', 
                 2: 'Wednesday', 
                 3: 'Thursday', 
                 4: 'Friday',
                 5: 'Saturday', 
                 6: 'Sunday'}
    

    study = ""
    start_time = ""
    end_time = ""
    day = ""
    contact = ""
    color = ""


    def __init__(self, title, start_time, end_time):
       
       #Since study ids can begin with either 2 letters or 3,
       #we have to see whether the title starts with 2 or 3 letters
       #before we assign a study to the event object
       three_letter_pattern = re.compile('^[A-Za-z][A-Za-z][A-Za-z]')
       two_letter_pattern = re.compile('^[A-Za-z][A-Za-z][0-9]')
       if three_letter_pattern.match(title):
           self.study = title[0:3]
       elif two_letter_pattern.match(title):
           self.study = title[0:2]
       #if you see N/A on the table, some didn't name their event correctly
       else:
           self.study = 'N/A'

       #converts the time data that google outputs into data we can use and convert to other formats
       #time.strptime takes a string representing a time and another string representing the format of the time string,
       #and does the conversion
       self.start_time = time.strptime(start_time, 
                                       "%Y-%m-%dT%H:%M:00.000-04:00")
       self.end_time = time.strptime(end_time, 
                                     "%Y-%m-%dT%H:%M:00.000-04:00")

       #pulls weekday from start time and converts it into the name of the day using out week_days dictionary
       self.day = self.week_days[self.start_time.tm_wday]

       #uses the study name and gets its contact from the contact dictionary
       self.contact = self.study_contacts[self.study]

       #does the same for the color
       self.color = self.study_colors[self.study]
       
       

       

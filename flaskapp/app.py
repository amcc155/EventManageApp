# Copyright © 2023, Indiana University
# BSD 3-Clause License

from flask import Flask, render_template
import csv
from operator import itemgetter
from datetime import datetime

app = Flask(__name__)

 
@app.route("/")
def index():
    return render_template("index.html")

#try to make this work with one function later
def get_events():
    ''' pull the events from the csv file, add to list, and sort them by time'''
    all_events = []
    with open('events.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            all_events.append(row)
        all_events_sorted = sorted(all_events, key = itemgetter('date','start_time'))
        #displaying the time in a 12 hour format instead of 24
        for event in all_events_sorted:
            event['start_time'] = datetime.strptime(event['start_time'], '%H:%M').strftime('%I:%M %p') #https://discuss.codecademy.com/t/how-to-convert-to-12-hour-clock/3920/3
    return all_events_sorted

def get_event_details():
    ''' use a dictionary comprehension to be able to call it later to access specific data'''
    with open('events.csv') as file:
        contents = csv.DictReader(file)
        all_events = {
            row['name']:{
                "name":row["name"],
                "date":row["date"],
                "venue":row["venue"],
                "start_time":row["start_time"],
                "end_time":row["end_time"],
                "invitation_text":row["invitation_text"],
                "image_path":row["image_path"],
                "max_attendees":row["max_attendees"],
                "party_planner":row["party_planner"],
                "rental_items":row["rental_items"],
                "notes":row["notes"],
            }
            for row in contents
        }
    return all_events

''' call the events function and render the events.html '''
@app.route("/events/")
def events():
    events = get_events()
    return render_template('events.html', events = events)

''' route the events with the event_id parameter, which takes the name of the event, which is used to access the data in the dictionary '''
@app.route("/events/<event_id>/")
def events_id(event_id: str):
    all_events = get_event_details()
    if event_id:
        return render_template('event.html', event = all_events[event_id])
 
''' function to create list of dictionary of venues, and sorting them from cheapest to lowest'''
def get_venues():
    event_list = []
    with open('venues.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['rental_fee'] = int(row["rental_fee"]) #converting to integer so it sorts correctly
            event_list.append(row)
        sorted_events = sorted(event_list, key = itemgetter('rental_fee'))
        return sorted_events

''' routing the venues which calls the get_venues function, which is then used in venues.html'''
@app.route("/venues/")
def venues():
    venues = get_venues()
    return(render_template('venues.html', venues = venues ))

''' function to get people, make it a list of dictionaries and sorting by oldest date of birth first'''
def get_people():
    people_list = []
    with open('people.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            people_list.append(row)
        sorted_people = sorted(people_list, key = itemgetter('date_of_birth') )
        return sorted_people
    
'''route people so it can take the people list of dicts, and use it in people.html'''
@app.route("/people/")
def people():
    people = get_people()
    return(render_template("people.html", people = people ))

# Copyright © 2023, Indiana University
# BSD 3-Clause License

from flask import Flask, render_template, request, redirect, url_for
import csv
from operator import itemgetter
from datetime import datetime

app = Flask(__name__)

 
@app.route("/")
def index():
    return render_template("index.html")

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
            try:
                datetime.strptime(event['start_time'], '%I:%M %p')
            except ValueError:
        # If the time is not in the 12-hour format, convert it to 12-hour format
                event['start_time'] = datetime.strptime(event['start_time'], '%H:%M').strftime('%I:%M %p')
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
    


def get_venues():
    ''' function to create list of dictionary of venues, and sorting them from cheapest to lowest'''
    event_list = []
    with open('venues.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['rental_fee'] = int(row["rental_fee"]) #converting to integer so it sorts correctly
            event_list.append(row)
        sorted_events = sorted(event_list, key = itemgetter('rental_fee'))
        return sorted_events
    

def get_people():
    ''' function to get people, make it a list of dictionaries and sorting by oldest date of birth first'''
    people_list = []
    with open('people.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            people_list.append(row)
        sorted_people = sorted(people_list, key = itemgetter('date_of_birth') )
        return sorted_people
    

def set_people(people):
    ''' function to write the people daata to the csv after the user adds a new one'''
    with open('people.csv', mode='w', newline='') as file:
        fieldnames = ['name','email','address','mobile_phone','date_of_birth']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(people)

    
'''route people so it can take the people list of dicts, and use it in people.html'''
@app.route("/people/")
def people():
    people = get_people()
    return(render_template("people.html", people = people ))

''' if user clicks submit button on form, get the form data and add it to the csv, otherwise bring user to form to fill out'''
@app.route("/people/add", methods = ['GET', "POST"])
def add_person():
    if request.method == "POST":
        people = get_people()
        new_person = {}

        new_person['name'] = request.form['name']
        new_person['address'] = request.form['address']
        new_person['email'] = request.form['email']
        new_person['mobile_phone'] = request.form['phone']
        new_person['date_of_birth'] = request.form['birth']
        
        people.append(new_person)
        print(f'people {people}')
        # Call the set_people function to write the updated list back to the CSV file
        set_people(people)
        return(redirect(url_for('index')))
    else:
        return(render_template('add-person.html'))
    
''' call the events function and render the events.html '''
@app.route("/events/")
def events():
    events = get_events()
    return render_template('events.html', events = events)

''' function to write all of the events into csv file after the user adds one'''
def set_events(events):
    with open('events.csv', mode = 'w', newline = '') as file:
        fieldnames = 'name','date','venue','start_time','end_time','invitation_text','image_path','max_attendees','party_planner','rental_items','notes'
        writer = csv.DictWriter(file, fieldnames = fieldnames)
        writer.writeheader()
        writer.writerows(events)

''' route the events with the event_id parameter, which takes the name of the event, which is used to access the data in the dictionary '''
@app.route("/events/<event_id>/")
def events_id(event_id: str):
    all_events = get_event_details()
    if event_id:
        return render_template('event.html', event = all_events[event_id])

''' either get the form data when the user submits add event form, or take the user to the form page if they click the add button'''
@app.route("/events/add", methods = ['GET',"POST"])
def add_event():
    if request.method == "POST":
        events = get_events()
        edited_event = {}

        edited_event['name'] = request.form['event_name']
        edited_event['venue'] = request.form['venue']
        edited_event['date'] = request.form['date']
        #convert the time here
        
        edited_event['start_time'] = request.form['start-time']
        edited_event['end_time'] = request.form['end-time']
        edited_event['max_attendees'] = request.form['max-attendees']
        edited_event['invitation_text'] = request.form['invitation']
        edited_event['party_planner'] = request.form['planner']
        edited_event['rental_items'] = request.form['rental-items']
        edited_event['image_path'] = request.form['image']
        edited_event['notes'] = request.form['notes']
        events.append(edited_event)
        set_events(events)
        return(redirect(url_for('index')))
    else:
        return(render_template('add-event.html'))

    
"Change the event data when the user clicks submit on the form, or bring them to the page to fill form out "
@app.route("/event/<event_id>/edit", methods = ['GET',"POST"])
def edit_event(event_id):
    all_events = get_event_details()
    events = get_events()
    edited_event = {}
    if request.method == "POST":
        edited_event['name'] = request.form['event_name']
        edited_event['venue'] = request.form['venue']
        edited_event['date'] = request.form['date']
        #converting time to 24 houur format so it can go through the get_events function when eventually called
        # start_time = datetime.strptime(request.form['start-time'], "%I:%M %p").strftime("%H:%M")
        # end_time = datetime.strptime(request.form['end-time'], "%I:%M %p").strftime("%H:%M")
        edited_event['start_time'] = request.form['start-time']
        edited_event['end_time'] = request.form['end-time']
        edited_event['max_attendees'] = request.form['max-attendees']
        edited_event['invitation_text'] = request.form['invitation']
        edited_event['party_planner'] = request.form['planner']
        edited_event['rental_items'] = request.form['rental-items']
        edited_event['image_path'] = request.form['image']
        edited_event['notes'] = request.form['notes']
        print(events)

        #delete the event the user is editing are editing so it can clear
        for event in events:
           if event['name'] == event_id:
                events.remove(event)
        
        #add the event back with the new details
        events.append(edited_event)
        set_events(events)
        
        
        return(redirect(url_for('index')))
    else:
        return(render_template('add-event.html', event_edit = all_events[event_id]))
    
''' routing the venues which calls the get_venues function, which is then used in venues.html'''
@app.route("/venues/")
def venues():
    venues = get_venues()
    return(render_template('venues.html', venues = venues ))

'''write all of the venues to the csv after the user adds a new one'''
def set_venue(venues):
    with open('venues.csv', mode = 'w', newline = '') as file:
        fieldnames = 'name','address','contact_phone','rental_fee','max_attendees'
        writer = csv.DictWriter(file,fieldnames)
        writer.writeheader()
        writer.writerows(venues)
    
''' if user hits submit on form, collect the data and add it to csv, othewise the user clicked the nav button bringing them to form'''
@app.route("/venue/add", methods = ['GET',"POST"])
def add_venue():
    if request.method == "POST":
        venues = get_venues()
        new_venue = {}
        new_venue['name'] = request.form['name']
        new_venue['address'] = request.form['address']
        new_venue['contact_phone'] = request.form['phone']
        new_venue['rental_fee'] = request.form['rental_fee']
        new_venue['max_attendees'] = request.form['max_attendees']
        venues.append(new_venue)
        set_venue(venues)

        
        return(redirect(url_for('index')))
    else:
        return(render_template("add-venue.html"))
    




    


# Copyright © 2023, Indiana University
# BSD 3-Clause License

from flask import Flask, render_template, request, redirect, url_for, flash
from operator import itemgetter
from datetime import datetime
from flaskapp import database
import re
import logging
app = Flask(__name__)

def validate_input(name, email, address, phone):
    errors = []
    # Name validation
    if len(name) > 50:
        errors.append('Name is too long')
    # Email validation
    email_pattern = r"^[a-z]{2,65}@[^\s]+\.\w{2,}$"
    if email is not None:
        if not re.match(email_pattern, email):
            errors.append('Invalid email')
    # Address validation
    if len(address) > 95:
        errors.append('Address is too long')
    address_pattern = r"\d+\s[A-Za-z0-9\s]+"
    #address pattern check
    if not re.match(address_pattern, address):
        errors.append('Address has invalid format')
    # Phone number validation
    phone_pattern = r"\(\d{3}\)[-|\s]?\d{3}[-|\s]?\d{4}"
    if not re.match(phone_pattern, phone):
        errors.append('Invalid phone number')

    return ' , '.join(errors)


@app.route("/")
def index():
    return render_template("index.html")

'''getting events list of dctionaries from database'''
def get_events():
    events = database.get_events()
    return events

def get_venues():
    venues = database.get_venues()
    return venues

'''getting people list of dicionaries from database'''
def get_people():
    people = database.get_people()
    return people

'''route people so it can take the people list of dicts, and use it in people.html'''
@app.route("/people/")
def display_people():
    people = database.get_people()
    for person in people:
        person['dob'] = datetime.strftime(person['dob'], '%m-%d-%y')
    return (render_template("people.html", people=people))

''' routing the venues which calls the get_venues function, which is then used in venues.html'''
@app.route("/venues/")
def display_venues():
    venues = database.get_venues()
    sorted_venues = sorted(venues, key=itemgetter('fee'))
    return (render_template('venues.html', venues=sorted_venues))


''' if user clicks submit button on form, get the form data and add it to the db, otherwise bring user to form to fill out'''
@app.route("/people/add", methods=['GET', "POST"])
def add_person():
    if request.method == "POST":
        #get data
        name = request.form['name']
        address = request.form['address']
        email = request.form['email']
        mobile_phone = request.form['phone']
        dob = request.form['birth']
        role = request.form['role']
        #handle data 
        error = validate_input(name, email, address, mobile_phone)
        if error:
            return render_template('add-person.html', error=error)
        else:
            database.add_person(name, address, email, dob, mobile_phone,role)
            return (redirect(url_for('display_people')))
    else:
        return (render_template('add-person.html'))


''' call the events function and render the events.html '''
@app.route("/events/")
def display_events():
    events = database.get_events()
    for event in events:
        event['event_date'] = datetime.strftime(event['event_date'], '%m-%d-%y')
    return render_template('events.html', events= events)


''' route the events with the event_id parameter, which takes the name of the event, which is used to access the data in the dictionary '''
@app.route("/events/<event_id>/")
def display_event(event_id: str):

    #getting data based of corresponding id
    event = database.get_event(event_id)
    name = database.get_venue_name(event_id)
    host = database.get_event_host(event_id)
    planner = database.get_event_planner(event_id)
    attendees = database.get_attendees(event_id)
    people = database.get_people()
    return render_template('event.html', event=event, name=name, host=host, planner=planner, attendees = attendees, people = people)


''' either get the form data when the user submits add event form, or take the user to the form page if they click the add button'''
@app.route("/events/add", methods=['GET', "POST"])
def add_event():
    venues = database.get_venues()
    people = database.get_people()
    if request.method == "POST":
        name = request.form['event_name']
        venue = request.form['venue']
        date = request.form['date']
        start_time = request.form['start-time']
        end_time = request.form['end-time']
        max_attendees = request.form['max-attendees']
        invitation = request.form['invitation']
        planner = request.form['planner']
        rental_items = request.form['rental-items']
        image_path = request.form['image']
        notes = request.form['notes']
        host = request.form['host']

        database.add_event(name, date, start_time, end_time, venue, invitation,
                           max_attendees, planner, host, rental_items, notes, image_path)

        return (redirect(url_for('display_events')))
    else:
        return(render_template('add-event.html', venues = venues, people = people))
    
    '''deleting attendees and redirecting back to event page'''
@app.route("/events/<event_id>/attendees/<person_id>/delete")
def delete_attendee(event_id, person_id):
    database.remove_attendee_event(event_id,person_id)
  
    return (redirect(url_for('display_event', event_id = event_id)))


#adding attendees and redirecting back to event page
@app.route("/events/<event_id>/attendees/add", methods = ['POST'])
def add_attendee(event_id):
    if request.method == 'POST':
        new_attendee_id = request.form['attendee']
     
        database.add_attendee_event(new_attendee_id,event_id)
    
    return(redirect(url_for('display_event', event_id = event_id)))
                
'''Change the event data when the user clicks submit on the form, or bring them to the page to fill form out'''
@app.route("/events/<event_id>/edit", methods=['GET', "POST"])
def edit_event(event_id):
    event = database.get_event(event_id)
    people = database.get_people()
    venues = database.get_venues()
    if request.method == "POST":
        name = request.form['event_name']
        venue = request.form['venue']
        date = request.form['date']
        start_time = request.form['start-time']
        end_time = request.form['end-time']
        max_attendees = request.form['max-attendees']
        invitation = request.form['invitation']
        planner = request.form['planner']
        rental_items = request.form['rental-items']
        image_path = request.form['image']
        notes = request.form['notes']
        host = request.form['host']

        #update the events
        database.update_event(event_id,name, date, start_time, end_time, venue, invitation,
                           max_attendees, planner, host, rental_items, notes, image_path)

        return (redirect(url_for('display_event', event_id = event_id)))
    else:
        return (render_template('add-event.html', event_edit=event, people = people, venues = venues))


''' if user hits submit on form, collect the data and add it to csv, othewise the user clicked the nav button bringing them to form'''
@app.route("/venue/add", methods=['GET', "POST"])
def add_venue():
    if request.method == "POST":
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']
        rental_fee = request.form['rental_fee']
        max_attendees = request.form['max_attendees']
        error = validate_input(name, None, address, phone)
        if error:
            return (render_template('add-venue.html', error=error))
        else:
            database.add_venues(name, address, phone,
                                rental_fee, max_attendees)
            return (redirect(url_for('display_venues')))
        
    else:
        return (render_template('add-venue.html'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
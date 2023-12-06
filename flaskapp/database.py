from pymysql import connect
from pymysql.cursors import DictCursor

from flaskapp.config import DB_HOST, DB_USER, DB_PASS, DB_DATABASE

# Make sure you have data in your tables. You should have used auto increment for
# primary keys, so all primary keys should start with 1


def get_connection():
    return connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_DATABASE,
        cursorclass=DictCursor,
    )


def get_events():
    sql = "select * from events order by event_date"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            events = cursor.fetchall()
            return events
            
"""Returns a list of dictionaries representing all of the event data"""

    

def get_event(event_id):
    sql = 'select * from events where event_id = %s'
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql,(event_id))
            return cursor.fetchone()
    """Takes a event_id, returns a single dictionary containing the data for the event with that id"""
    
def get_venue_name(event_id):
    sql = 'select venue.name from venue JOIN events as e on e.venue = venue_id WHERE event_id = %s'
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql,(event_id))
            return cursor.fetchone()
        
def get_event_host(event_id):
    sql = 'select people.* from people JOIN events as e on e.host = people.person_id WHERE event_id = %s '
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql,(event_id))
            return cursor.fetchone()  

def get_event_planner(event_id):
    sql = 'select people.* from people JOIN events as e on e.planner = people.person_id WHERE event_id = %s'
    conn= get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql,(event_id))
            return cursor.fetchone()

            
def add_event(name,event_date,start_time,end_time,venue,invitation,maximum_attendees,planner,host,rental_items,notes,image_path):
    """Takes as input all of the data for a event. Inserts a new event into the event table"""
    sql = "insert into events(name,event_date,start_time,end_time,venue,invitation,maximum_attendees,planner,host,rental_items,notes,image_path) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql,(name,event_date,start_time,end_time,venue,invitation,maximum_attendees,planner,host,rental_items,notes,image_path))
        conn.commit()
   

def update_event(event_id, name,event_date,start_time,end_time,venue,invitation,maximum_attendees,planner,host,rental_items,notes,image_path):
    """Takes a event_id and data for a event. Updates the event table with new data for the event with event_id as it's primary key"""
    sql = "UPDATE events SET name = %s, event_date = %s, start_time = %s, end_time = %s, venue = %s, invitation = %s, maximum_attendees = %s, planner = %s, host = %s, rental_items = %s, notes = %s, image_path = %s WHERE event_id = %s"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (name, event_date, start_time, end_time, venue, invitation, maximum_attendees, planner, host, rental_items, notes, image_path, event_id))
        conn.commit()
  
def get_people():
    sql = "SELECT * FROM people ORDER BY dob"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            people = cursor.fetchall()
            return people
    """Returns a list of dictionaries representing all of the person data"""
    

def add_person(name,address,email,dob,phone):
    sql = 'INSERT INTO people(name, address, email, dob, phone) VALUES (%s, %s, %s, %s, %s)'
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql,(name,address, email, dob, phone))
        conn.commit()
        
    """Takes as input all of the data for a person and adds a new person to the person table"""
   

def delete_person(person_id):
    sql = "DELETE FROM people WHERE person_id = %s"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (person_id))
        conn.commit()
    
        

    """Takes a person_id and deletes the person with that person_id from the person table"""
    pass

def get_attendees(event_id):
    """Returns a list of dictionaries representing all of the data for people attending a particular event"""
    sql = 'SELECT people.* FROM people, attendees WHERE people.person_id = attendees.attendee_id AND attendees.event_id = %s'
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql,(event_id))
            return cursor.fetchall()
    
    

def add_attendee_event(event_id, attendee_id):
    """Takes as input a event_id and a attendee_id and inserts the appropriate data into the database that indicates the attendee with attendee_id as a primary key is attending the event with the event_id as a primary key"""
    sql = "INSERT INTO attendees(attendee_id, event_id) VALUES (%s %s)"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql,(attendee_id, event_id))
        conn.commit()
    

def remove_attendee_event(event_id, attendee_id):
    """Takes as input a event_id and a attendee_id and deletes the data in the database that indicates that the attendee with attendee_id as a primary key
    is attending the event with event_id as a primary key."""
    sql = 'DELETE FROM attendees WHERE event_id = %s and attendee_id = %s'
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql,(event_id,attendee_id))
        conn.commit()


def get_host(event_id):
    """Takes a event_id and returns a dictionary of the data for the host of the event with
    event_id as its primary key"""
    sql = 'SELECT people.* FROM people JOIN events AS e ON e.host = people.person_id WHERE e.event_id = %s;'
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql,(event_id))
            return cursor.fetchone()

    
def set_host(person_id, event_id):
    """Sets the person with primary key person_id as the host of the event with event_id as its primary key"""
    sql = 'UPDATE events SET host = %s WHERE event_id = %s '
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql,(person_id, event_id))
        conn.commit()

    

def get_planner(event_id):
    """Takes a event_id and returns a dictionary of the data for the planner of the event with
    event_id as its primary key"""
    sql = 'SELECT people.* FROM people JOIN events as e ON people.person_id = e.planner WHERE e.event_id = %s '
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql,(event_id))
            return cursor.fetchone()

    

def set_planner(person_id, event_id):
    """Sets the person with primary key person_id as the planner of the event with event_id as its primary key"""
    sql = "UPDATE events SET planner = %s WHERE event_id = %s"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql,(person_id, event_id))
        conn.commit()


def get_venues():
    """Returns a list of dictionaries representing all of the venues data"""
    sql = 'SELECT * FROM venues ORDER BY fee '
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
        
    

def add_venues(name,address,phone,fee,capacity):
    """Takes as input all of the data for a venue. Inserts a new venue into the event table"""
    sql = 'INSERT INTO venues(name,address,phone,fee,maximum_attendees) VALUES(%s, %s, %s, %s, %s)'
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql,(name,address,phone,fee,capacity))
        conn.commit()


if __name__ == "__main__":
    # Add test code here to make sure all your functions are working correctly
    
   
    
    print(get_event(2))
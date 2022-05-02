from tinydb import TinyDB
from datetime import datetime

# Create the db files
users_db = TinyDB('./db/users.json')
meetings_db = TinyDB('./db/meetings.json')
meeting_instances_db = TinyDB('./db/meeting_instances.json')
eventsLogs_db = TinyDB('./db/eventsLogs.json')

# Insert the data into the users database
users_db.insert({'userID': 1, 'name': 'Rick Sanchez', 'age': 65, 'gender': 'Male', 'email': 'rsanchez@mail.com'})
users_db.insert({'userID': 2, 'name': 'Harry Potter', 'age': 19, 'gender': 'Male', 'email': 'hpotter@mail.com'})
users_db.insert({'userID': 3, 'name': 'Pam Beesly', 'age': 31, 'gender': 'Female', 'email': 'pbeesly@mail.com'})
users_db.insert({'userID': 4, 'name': 'Rachel Green', 'age': 46, 'gender': 'Female', 'email': 'rgreen@mail.com'})
users_db.insert({'userID': 5, 'name': 'Lewis Hamilton', 'age':37, 'gender': 'Male', 'email': 'lhamilton@mail.com'})

# Insert the data into the meetings database
meetings_db.insert({'meetingID': 1, 'title': 'Green Chemistry', 
    'description': 'A meeting to discuss about the current trends in environmentally friendly chemistry', 
    'isPublic': True, 'audience': [2, 1]})
meetings_db.insert({'meetingID': 2, 'title': 'Deep Learning & NLP', 
    'description': 'A meeting to discuss about the state-of-art neural network architectures for language models', 
    'isPublic': True, 'audience': [2, 3, 4]})
meetings_db.insert({'meetingID': 3, 'title': 'Cryptocurrencies & Blockchain', 
    'description': 'A meeting to discuss about the upcoming crypto projects, that will dominate the economy', 
    'isPublic': False, 'audience': [5, 1, 4]})
meetings_db.insert({'meetingID': 4, 'title': 'Metaverse', 
    'description': 'A meeting to discuss about the possible applications of the metaverse', 
    'isPublic': True, 'audience': [3, 5]})

# Insert the data into the meeting_instances database
meeting_instances_db.insert({'meetingID': 1, 'orderID': 1, 'fromdatetime': datetime(2022,5,3,12,30,0,0).isoformat(), 'todatetime': datetime(2022,5,3,15,30,0,0).isoformat()})
meeting_instances_db.insert({'meetingID': 2, 'orderID': 1, 'fromdatetime': datetime(2022,5,4,12,30,0,0).isoformat(), 'todatetime': datetime(2022,5,4,16,0,0,0).isoformat()})
meeting_instances_db.insert({'meetingID': 3, 'orderID': 1, 'fromdatetime': datetime(2022,5,4,17,0,0,0).isoformat(), 'todatetime': datetime(2022,5,4,19,0,0,0).isoformat()})
meeting_instances_db.insert({'meetingID': 4, 'orderID': 1, 'fromdatetime': datetime(2022,5,5,11,0,0,0).isoformat(), 'todatetime': datetime(2022,5,5,13,30,0,0).isoformat()})
meeting_instances_db.insert({'meetingID': 1, 'orderID': 2, 'fromdatetime': datetime(2022,5,6,12,0,0,0).isoformat(), 'todatetime': datetime(2022,5,6,14,30,0,0).isoformat()})
meeting_instances_db.insert({'meetingID': 3, 'orderID': 2, 'fromdatetime': datetime(2022,5,8,12,30,0,0).isoformat(), 'todatetime': datetime(2022,5,8,15,30,0,0).isoformat()})
meeting_instances_db.insert({'meetingID': 2, 'orderID': 2, 'fromdatetime': datetime(2022,5,9,13,0,0,0).isoformat(), 'todatetime': datetime(2022,5,9,15,0,0,0).isoformat()})

# Insert the data into the eventsLogs database
eventsLogs_db.insert({'event_id': 1, 'userID': 1, 'event_type': 1, 'timestamp': datetime(2022,5,3,12,30,0,0).isoformat()})
eventsLogs_db.insert({'event_id': 2, 'userID': 4, 'event_type': 1, 'timestamp': datetime(2022,5,3,12,30,0,0).isoformat()})
eventsLogs_db.insert({'event_id': 3, 'userID': 3, 'event_type': 1, 'timestamp': datetime(2022,5,3,12,30,0,0).isoformat()})
eventsLogs_db.insert({'event_id': 4, 'userID': 2, 'event_type': 1, 'timestamp': datetime(2022,5,3,12,30,0,0).isoformat()})
eventsLogs_db.insert({'event_id': 5, 'userID': 5, 'event_type': 1, 'timestamp': datetime(2022,5,3,12,30,0,0).isoformat()})
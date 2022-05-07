import sqlite3
  
# connecting to the database
connection = sqlite3.connect("redis.db")
  
# cursor
crsr = connection.cursor()

print("Connected to the database")

# drop tables to re-initiate
drop_tables = """DROP TABLE eventsLogs;
DROP TABLE meeting_instances;
DROP TABLE meetings;
DROP TABLE users;"""

# create the db tables
users_table = """CREATE TABLE users ( 
userID INTEGER PRIMARY KEY, 
name VARCHAR(50), 
age INTEGER, 
gender CHAR(10), 
email CHAR(50));"""

meetings_table = """CREATE TABLE meetings ( 
meetingID INTEGER PRIMARY KEY, 
title VARCHAR(50), 
description VARCHAR(200), 
isPublic BOOLEAN, 
audience CHAR(50));"""

meeting_instances_table = """CREATE TABLE meeting_instances ( 
meetingID INTEGER, 
orderID INTEGER, 
fromdatetime DATETIME, 
todatetime DATETIME, 
CONSTRAINT meeting_instances_PK PRIMARY KEY (meetingID, orderID),
FOREIGN KEY (meetingID) REFERENCES meetings(meetingID));"""

eventsLogs_table = """CREATE TABLE eventsLogs ( 
event_id INTEGER PRIMARY KEY, 
userID INTEGER, 
event_type VARCHAR(50), 
timestamp DATETIME,
FOREIGN KEY (userID) REFERENCES users(userID));"""

# insert the data into the tables
insert_users = """
INSERT INTO users
  (userID, name, age, gender, email)
VALUES
  (1, 'Rick Sanchez', 65, 'Male', 'rsanchez@mail.com'), 
  (2, 'Harry Potter', 19, 'Male', 'hpotter@mail.com'),
  (3, 'Pam Beesly', 31, 'Female', 'pbeesly@mail.com'),
  (4, 'Rachel Green', 46, 'Female', 'rgreen@mail.com'),
  (5, 'Lewis Hamilton', 37, 'Male', 'lhamilton@mail.com');"""

insert_meetings = """
INSERT INTO meetings
  (meetingID, title, description, isPublic, audience)
VALUES
  (1, 'Green Chemistry', 'A meeting to discuss about the current trends in environmentally friendly chemistry', TRUE, '2,1'), 
  (2, 'Deep Learning & NLP', 'A meeting to discuss about the state-of-art neural network architectures for language models', TRUE, '2,3,4'),
  (3, 'Cryptocurrencies & Blockchain', 'A meeting to discuss about the upcoming crypto projects, that will dominate the economy', FALSE, '5,1,4'),
  (4, 'Metaverse', 'A meeting to discuss about the possible applications of the metaverse', TRUE, '3,5');"""

insert_meeting_instances = """
INSERT INTO meeting_instances
  (meetingID, orderID, fromdatetime, todatetime)
VALUES
  (1, 1, '2022-05-03 12:30:00', '2022-05-03 15:30:00'), 
  (2, 1, '2022-05-04 12:30:00', '2022-05-04 16:00:00'),
  (3, 1, '2022-05-04 17:00:00', '2022-05-04 19:00:00'),
  (4, 1, '2022-05-05 11:00:00', '2022-05-05 13:30:00'),
  (1, 2, '2022-05-06 12:00:00', '2022-05-06 14:30:00'),
  (3, 2, '2022-05-08 12:30:00', '2022-05-08 15:30:00'),
  (2, 2, '2022-05-09 13:00:00', '2022-05-09 15:00:00');"""

# execute the statements
crsr.executescript(drop_tables)
crsr.execute(users_table)
crsr.execute(meetings_table)
crsr.execute(meeting_instances_table)
crsr.execute(eventsLogs_table)
crsr.execute(insert_users)
crsr.execute(insert_meetings)
crsr.execute(insert_meeting_instances)

connection.commit()

# close the connection
connection.close()
from tinydb import Query, TinyDB
from datetime import datetime
import redis

# Get the data from the databases
users_db = TinyDB('./db/users.json')
meetings_db = TinyDB('./db/meetings.json')
meeting_instances_db = TinyDB('./db/meeting_instances.json')
eventsLogs_db = TinyDB('./db/eventsLogs.json')

# Initialize the redis object
r = redis.Redis(host= 'localhost',port= '6379', charset="utf-8", decode_responses=True)

# Initialize the query object
q = Query()

def activate_meeting():
    meetingID = input('Enter the meeting ID: ')
    orderID = input('Enter the order ID: ')

    if meeting_instances_db.search((q.meetingID == int(meetingID)) & (q.orderID == int(orderID))):

        m = meetingID + ":" + orderID

        if r.sismember('active_meetings', m):
            print('Already activated!')
            return
        else:
            r.sadd('active_meetings', m)
            print('Meeting ' + m + ' activated!')
            return
    else:
            print('Meeting does not exist!')


def join_active_meeting():
    userID = input('Enter the user ID: ')

    if users_db.search(q.userID == int(userID)):
        meetingID = input('Enter the meeting ID: ')
        orderID = input('Enter the order ID: ')

        if meeting_instances_db.search((q.meetingID == int(meetingID)) & (q.orderID == int(orderID))):
            m = meetingID + ":" + orderID

            if not r.sismember('active_meetings', m):
                print('Meeting not active!')
                return
            else:
                if meetings_db.search((q.meetingID == int(meetingID)) & (q.audience.any([int(userID)]))):
                    k = 'meeting:' + m

                    if r.sismember(k, userID):
                        print('Already joined!')
                        return
                    else:
                        r.sadd(k, userID)
                        print('User ' + userID + ' joined the meeting ' + meetingID + ':' + orderID)
                        return
                else:
                    print('The user is not in the audience!')
                    return
        else:
            print('Meeting does not exist!')
            return
    else:
        print('The user does not exist!')


def leave_meeting():
    userID = input('Enter the user ID: ')

    if users_db.search(q.userID == int(userID)):
        meetingID = input('Enter the meeting ID: ')
        orderID = input('Enter the order ID: ')

        if meeting_instances_db.search((q.meetingID == int(meetingID)) & (q.orderID == int(orderID))):
            m = meetingID + ":" + orderID

            if not r.sismember('active_meetings', m):
                print('Meeting not active!')
                return
            else:
                k = 'meeting:' + m

                if not r.sismember(k, userID):
                    print('Not in the meeting!')
                    return
                else:
                    r.srem(k, userID)
                    print('User ' + userID + ' left the meeting ' + meetingID + ':' + orderID)
                    return
        else:
            print('Meeting does not exist!')
            return
    else:
        print('The user does not exist!')


def show_participants():
    meetingID = input('Enter the meeting ID: ')
    orderID = input('Enter the order ID: ')

    if meeting_instances_db.search((q.meetingID == int(meetingID)) & (q.orderID == int(orderID))):
        m = meetingID + ":" + orderID

        if not r.sismember('active_meetings', m):
            print('Meeting not active!')
            return
        else:
            k = 'meeting:' + m
            participants = r.smembers(k)
            print('Meeting\'s ' + m + ' participants:')

            if len(participants) == 0:
                print('Empty meeting!')
            else:
                for i in participants:
                    print('User:', i)
    else:
        print('Meeting does not exist!')
        return


def show_active_meetings():
    active_meetings = r.smembers('active_meetings')

    if len(active_meetings) == 0:
        print('No active meetings!')
    else:
        print('Active meetings:')
        for i in active_meetings:
            print('Meeting:', i)


def end_meeting():
    meetingID = input('Enter the meeting ID: ')
    orderID = input('Enter the order ID: ')

    if meeting_instances_db.search((q.meetingID == int(meetingID)) & (q.orderID == int(orderID))):
        m = meetingID + ":" + orderID
        if not r.sismember('active_meetings', m):
            print('Meeting not active!')
            return
        else:
            r.srem('active_meetings', m)
            k = 'meeting:' + m
            r.delete(k)
            print('Meeting ' + m + ' ended and all participants left!')
            return
    else:
        print('Meeting does not exist!')


def post_chat_message():
    pass


def show_meeting_chat():
    pass


def show_active_meetings_participants_join_time():
    pass


def show_active_meeting_user_messages():
    pass


# activate_meeting(6,3)
# a = show_active_meetings()
# print(a)
# print(r.smembers('meeting:1:6'))
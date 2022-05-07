from datetime import datetime
import redis
import sqlite3

# connecting to the database
connection = sqlite3.connect("redis.db")
crsr = connection.cursor()

# Initialize the redis object
r = redis.Redis(host= 'localhost',port= '6379', charset="utf-8", decode_responses=True)

# The current number of events staring from one
eventlog_num = 1


def activate_meeting():
    meetingID = input('Enter the meeting ID: ')
    orderID = input('Enter the order ID: ')

    crsr.execute("SELECT meetingID, orderID FROM meeting_instances")
    ans = crsr.fetchall()

    if (int(meetingID), int(orderID)) in ans:

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

    crsr.execute("SELECT userID FROM users")
    ans = crsr.fetchall()

    if (int(userID),) in ans:
        meetingID = input('Enter the meeting ID: ')
        orderID = input('Enter the order ID: ')

        crsr.execute("SELECT meetingID, orderID FROM meeting_instances")
        ans = crsr.fetchall()

        if (int(meetingID), int(orderID)) in ans:
            m = meetingID + ":" + orderID

            if not r.sismember('active_meetings', m):
                print('Meeting not active!')
                return
            else:
                crsr.execute("SELECT audience FROM meetings WHERE meetingID =?", [meetingID])
                ans = crsr.fetchall()

                if userID in ans[0][0].split(',') :
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


def add_eventlog(userID, event_type):
    global eventlog_num
    eventsLogs_db.insert({'event_id': eventlog_num, 'userID': userID , 'event_type': event_type, 'timestamp': datetime.now().isoformat()})
    eventlog_num +=1
    return
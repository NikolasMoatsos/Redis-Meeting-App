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
    meetings_ans = crsr.fetchall()

    if (int(meetingID), int(orderID)) in meetings_ans:

        m = meetingID + ":" + orderID

        if not r.sismember('active_meetings', m):
            r.sadd('active_meetings', m)
            print('Meeting ' + m + ' activated!')
            return
        else:
            print('Already activated!')
            return
    else:
        print('Meeting does not exist!')
        return
        
        
def join_active_meeting():
    userID = input('Enter the user ID: ')

    crsr.execute("SELECT userID FROM users")
    users_ans = crsr.fetchall()

    if (int(userID),) in users_ans:
        meetingID = input('Enter the meeting ID: ')
        orderID = input('Enter the order ID: ')

        crsr.execute("SELECT meetingID, orderID FROM meeting_instances")
        meetings_ans = crsr.fetchall()

        if (int(meetingID), int(orderID)) in meetings_ans:
            m = meetingID + ":" + orderID

            if r.sismember('active_meetings', m):
                crsr.execute("SELECT audience FROM meetings WHERE meetingID =?", [meetingID])
                audience_ans = crsr.fetchall()

                crsr.execute("SELECT email,name FROM users WHERE userID =?", [userID])
                user_ans = crsr.fetchall()

                if user_ans[0][0] in audience_ans[0][0].split(',') :
                    # k = 'meeting:' + m
                    m_key_hash_join = 'meeting:' + meetingID + ':order:' + orderID + ':join'

                    if not r.hexists(m_key_hash_join, userID):
                        now = round(datetime.timestamp(datetime.now()))
                        r.hset(m_key_hash_join, userID, now)
                        # r.sadd(k, userID)
                        print('User ' + user_ans[0][1] + ' joined the meeting ' + meetingID + ':' + orderID)
                        return
                    else:
                        print('Already joined!')
                        return
                else:
                    print('The user is not in the audience!')
                    return
            else:
                print('Meeting not active!')
                return
        else:
            print('Meeting does not exist!')
            return
    else:
        print('The user does not exist!')
        return


def leave_meeting():
    userID = input('Enter the user ID: ')

    crsr.execute("SELECT userID FROM users")
    users_ans = crsr.fetchall()

    if (int(userID),) in users_ans:
        meetingID = input('Enter the meeting ID: ')
        orderID = input('Enter the order ID: ')

        crsr.execute("SELECT meetingID, orderID FROM meeting_instances")
        meetings_ans = crsr.fetchall()

        if (int(meetingID), int(orderID)) in meetings_ans:
            m = meetingID + ":" + orderID

            if r.sismember('active_meetings', m):
                # k = 'meeting:' + m
                m_key_hash_join = 'meeting:' + meetingID + ':order:' + orderID + ':join'

                if r.hexists(m_key_hash_join, userID):
                    # r.srem(k, userID)
                    r.hdel(m_key_hash_join, userID)
                    print('User ' + userID + ' left the meeting ' + meetingID + ':' + orderID)
                    return  
                else:
                    print('Not in the meeting!')
                    return
            else:
                print('Meeting not active!')
                return
        else:
            print('Meeting does not exist!')
            return
    else:
        print('The user does not exist!')
        return


def show_participants():
    meetingID = input('Enter the meeting ID: ')
    orderID = input('Enter the order ID: ')

    crsr.execute("SELECT meetingID, orderID FROM meeting_instances")
    meetings_ans = crsr.fetchall()

    if (int(meetingID), int(orderID)) in meetings_ans:
        m = meetingID + ":" + orderID

        if r.sismember('active_meetings', m):
            # k = 'meeting:' + m
            m_key_hash_join = 'meeting:' + meetingID + ':order:' + orderID + ':join'
            participants = r.hgetall(m_key_hash_join)

            if len(participants) > 0:
                print('Meeting\'s ' + m + ' participants:')
                for i in participants.keys():
                    print('User:', i)
                return
            else:
                print('Empty meeting!')
                return
        else:
            print('Meeting not active!')
            return   
    else:
        print('Meeting does not exist!')
        return


def show_active_meetings():
    active_meetings = r.smembers('active_meetings')

    if len(active_meetings) > 0:
        print('Active meetings:')
        for i in active_meetings:
            print('Meeting:', i)
        return
    else:
        print('No active meetings!')
        return


def end_meeting():
    meetingID = input('Enter the meeting ID: ')
    orderID = input('Enter the order ID: ')
    
    crsr.execute("SELECT meetingID, orderID FROM meeting_instances")
    meetings_ans = crsr.fetchall()

    if (int(meetingID), int(orderID)) in meetings_ans:
        m = meetingID + ":" + orderID

        if r.sismember('active_meetings', m):
            r.srem('active_meetings', m)

            # k = 'meeting:' + m
            m_key_hash_join = 'meeting:' + meetingID + ':order:' + orderID + ':join'
            keys_del = r.hgetall(m_key_hash_join).keys()
            r.hdel(m_key_hash_join, *keys_del)
            # r.delete(k)
            print('Meeting ' + m + ' ended and all participants left!')
            return
        else:
            print('Meeting not active!')
            return           
    else:
        print('Meeting does not exist!')
        return


def post_chat_message():
    meetingID = input('Enter the meeting ID: ')
    orderID = input('Enter the order ID: ')

    crsr.execute("SELECT meetingID, orderID FROM meeting_instances")
    meetings_ans = crsr.fetchall()

    if (int(meetingID), int(orderID)) in meetings_ans:
        m = meetingID + ":" + orderID
    
        if r.sismember('active_meetings', m):
            userID = input('Enter the user ID: ')

            crsr.execute("SELECT userID FROM users")
            users_ans = crsr.fetchall()

            if (int(userID),) in users_ans:
                # k = 'meeting:' + m
                m_key_hash_join = 'meeting:' + meetingID + ':order:' + orderID + ':join'

                if  r.hexists(m_key_hash_join, userID):
                    message = input('Type the message: ')
                    message_id = str(r.incr(m, 1))
                    m_key_hash_message = 'meeting:' + meetingID + ':order:' + orderID + ':messages'
                    m_key_hash_user = 'meeting:' + meetingID + ':order:' + orderID + ':user'
                    m_key_list = 'meeting:' + meetingID + ':order:' + orderID + ':message_order'

                    r.hset(m_key_hash_message, message_id, message)
                    r.hset(m_key_hash_user, message_id, userID)
                    r.rpush(m_key_list,message_id)
                    return
                else:
                    print('Not in the meeting!')
                    return
            else:
                print('The user does not exist!')
                return 
        else:
            print('Meeting not active!')
            return
    else:
        print('Meeting does not exist!')
        return
 


def show_meeting_chat():
    meetingID = input('Enter the meeting ID: ')
    orderID = input('Enter the order ID: ')

    crsr.execute("SELECT meetingID, orderID FROM meeting_instances")
    meetings_ans = crsr.fetchall()

    if (int(meetingID), int(orderID)) in meetings_ans:
        m = meetingID + ":" + orderID
    
        if r.sismember('active_meetings', m):
            m_key_hash_message = 'meeting:' + meetingID + ':order:' + orderID + ':messages'
            m_key_list = 'meeting:' + meetingID + ':order:' + orderID + ':message_order'
            chat_order = r.lrange(m_key_list, 0, -1)

            if len(chat_order) > 0:
                print('{} Meeting Chat:'.format(m))
                for i in range(len(chat_order)):
                    print('Message {}: {}'.format(i + 1, r.hget(m_key_hash_message, chat_order[i])))
                return
            else:
                print('No messages in the chat!')
                return
        else:
            print('Meeting not active!')
            return
    else:
        print('Meeting does not exist!')
        return


def show_active_meetings_participants_join_time():
    activate_meetings = r.smembers('active_meetings')

    if len(activate_meetings) > 0:
        
        for meeting in activate_meetings:
            print('Meeting {}:'.format(meeting))
            ids = meeting.split(':')
            m = 'meeting:' + ids[0] + ':order:' + ids[1] + ':join'
            joins = r.hgetall(m)

            if len(joins) > 0:
                for user,time in joins.items():
                    print('User {} joined at {}'.format(user,datetime.fromtimestamp(int(time))))
            else:
                print('No user joined this meeting!')
    else:
        print('No active meetings')


def show_active_meeting_user_messages():
    meetingID = input('Enter the meeting ID: ')
    orderID = input('Enter the order ID: ')

    crsr.execute("SELECT meetingID, orderID FROM meeting_instances")
    meetings_ans = crsr.fetchall()

    if (int(meetingID), int(orderID)) in meetings_ans:
        m = meetingID + ":" + orderID
    
        if r.sismember('active_meetings', m):
            userID = input('Enter the user ID: ')

            crsr.execute("SELECT userID FROM users")
            users_ans = crsr.fetchall()

            if (int(userID),) in users_ans:
                m_key_hash_join = 'meeting:' + meetingID + ':order:' + orderID + ':join'

                if  r.hexists(m_key_hash_join, userID):
                    m_key_hash_message = 'meeting:' + meetingID + ':order:' + orderID + ':messages'
                    chat = r.hgetall(m_key_hash_message).keys()
                    
                    if len(chat) > 0:
                        m_key_hash_user = 'meeting:' + meetingID + ':order:' + orderID + ':user'
                        c = 0
                        print('Messages from user {}:'.format(userID))
                        for key in chat:
                            if str(r.hget(m_key_hash_user,key)) == userID:
                                c += 1 
                                print('Message {}: {}'.format(c, r.hget(m_key_hash_message, key)))
                        if c == 0:
                            print('This user has not posted any messages yet!')
                        return 
                    else:
                        print('No messages in the chat!')
                        return
                else:
                    print('Not in the meeting!')
                    return 
            else:
                print('The user does not exist!') 
                return 
        else:
            print('Meeting not active!')
            return 
    else:
        print('Meeting does not exist!')
        return


# def add_eventlog(userID, event_type):
#     global eventlog_num
#     eventsLogs_db.insert({'event_id': eventlog_num, 'userID': userID , 'event_type': event_type, 'timestamp': datetime.now().isoformat()})
#     eventlog_num +=1
#     return

# crsr.execute("SELECT fromdatetime FROM meeting_instances WHERE meetingID =? AND orderID =?", [1,1])
# meeting_ans = crsr.fetchall()
# print(meeting_ans)
# print(r.hget('meeting:1:order:1:messages', 'message:7'))
# print(str(r.incr('1:1', 1)))
# print(r.hget('meeting:1:order:1:user',1))
# print(datetime.timestamp(datetime.now()))
# print(r.smembers('active_meetings'))
# m = 'meeting:' + '1' + ':order:' + '1' + ':join'
# a= r.hgetall(m)
# for j in a.keys():
#     print(j)
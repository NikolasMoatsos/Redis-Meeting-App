import functions


def main():
    print('Welcome to the Redis Meeting App!')

    end = False
    while end == False:
        print('\nMenu: \
                \n1)Activate a meeting \
                \n2)Join an active meeting \
                \n3)Leave a meeting \
                \n4)Show meeting’s current participants \
                \n5)Show active meetings \
                \n6)End a meeting \
                \n7)Post a message \
                \n8)Show a meeting\'s chat \
                \n9)Show the join time of the users \
                \n10)Show all messages from a specific user in meeting \
                \n11)Exit')
        selection = input('Select an option: ')
        print('')
        # try:
        if selection == '1':
            functions.activate_meeting()
        elif selection == '2':
            functions.join_active_meeting()
        elif selection == '3':
            functions.leave_meeting()
        elif selection == '4':
            functions.show_participants()
        elif selection == '5':
            functions.show_active_meetings()
        elif selection == '6':
            functions.end_meeting()
        elif selection == '7':
            functions.post_chat_message()
        elif selection == '8':
            functions.show_meeting_chat()
        elif selection == '9':
            functions.show_active_meetings_participants_join_time()
        elif selection == '10':
            functions.show_active_meeting_user_messages()
        elif selection == '11':
            end = True
        else:
            print('Not valid option!')
        # except Exception:
        #     print('Something went wrong! Going back to the menu.')

main()
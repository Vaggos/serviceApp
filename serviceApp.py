#!/usr/bin/python3

# This program is distributed under the GPLv2 license.

# @Author: Vagelis Prokopiou
# @Email: drz4007@gmail.com

import csv
import datetime
import random
import re


def validate_date(user_date, today):
    """
    Checks diff of provided date in comparison to today.
    """
    year, month, day = user_date.strip().split('-')
    date = datetime.date(int(year), int(month), int(day))
    if (today > date) and ((today - date) > datetime.timedelta(days=547)):
        return -1
    if today < date:
        return 1
    return 0


def regex_validate_date(date):
    """
    Validates that the data provided is a date.
    """
    m = re.search("^(\d{4})-(\d{2})-(\d{2})$", date)
    return m


def regex_validate_num(num):
    """
    Validates that the data provided is a number.
    """
    m = re.search("^\d+?$", num)
    if m is None:
        return False
    return True


def regex_validate_string(s):
    """
    Validates that the data provided is a number.
    """
    m = re.search("^[A-Z|a-z]+?$", s)
    if m is None:
        return False
    return True


def create_date_object(str_date):
    """
    Turns the user dates to date objects.
    """
    try:
        year, month, day = str_date.split('-')
        date = datetime.date(int(year), int(month), int(day))
        return date
    except Exception as e:
        print(e)
        return False


def create_delta_object(date_diff):
    """
    Creates a datetime delta object.
    """
    days = int(date_diff) * 30
    target_date = datetime.timedelta(days=days)
    return target_date


def compare_dates(date_changed, date_current, date_interval):
    """
    Checks the difference between dates.
    """
    date = create_date_object(date_changed)
    interval = create_delta_object(date_interval)
    if (date_current - date) >= interval:
        return True
    return False


def compare_kms(kms_current, kms_changed, kms_interval):
    """
    Checks the difference between kilometers.
    """
    kms_changed = int(kms_changed)
    kms_interval = int(kms_interval)
    if (kms_current - kms_changed) >= kms_interval:
        return True
    return False


def update_entry(choice, user_date, user_kms, spare_parts_list):
    """
    Updates an existing entry.
    """
    for x in range(len(spare_parts_list)):
        if spare_parts_list[x][0] == choice:
            spare_parts_list[x][1] = str(user_date)
            spare_parts_list[x][3] = str(user_kms)
            write_data(spare_parts_list)


def write_data(spare_parts_list):
    """
    Writes to the "data.csv" file.
    """
    with open('data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerows(spare_parts_list)
    print('\nThe data was updated successfully. Thank you.\n')


def inspection_msg(messages):
    """
    Prints the messages produced by the inspection.
    """
    if messages:
        for x in range(len(messages)):
            print('\n' + messages[x])
    else:
        print('\nYou rock! Everything looks good!\nRun me again in a few days, will \'ya? :)')


def error_msg(errors, errors_advanced, tries):
    """
    Prints the various error messages.
    """
    if tries < len(errors):
        return errors[tries]
    return errors_advanced[random.randint(0, (len(errors_advanced) - 1))]


def inform(spare_parts_list):
    """
    Informs the user for the currently available data entries in the "data.csv" file.
    """
    print('\nCurrently, the available data entries are the following:\n')
    for x in range(1, len(spare_parts_list)):
        print('{0}: Last changed on {1}. Must be changed every {2} months, or every {3} kilometers.\n'.format(
            spare_parts_list[x][0], spare_parts_list[x][1], spare_parts_list[x][2], spare_parts_list[x][4]))


def main():
    """
    The main function/program.
    """
    # A list with various, custom error messages.
    error_messages = ['Your input is wrong. Please try again.',
                      'Wrong again...',
                      'Wrong again... Really?',
                      'I am losing my patience...',
                      'Wrong again. Are you retarded man?',
                      'This is insane!!!',
                      'Are you kidding me?',
                      ]

    error_messages_advanced = ['Arggggg!!!!!!!!!',
                               'What an @$$!!!',
                               'Are you sure that you are mentally ok man?\nMaybe you should check it out...',
                               'It seems that you should be starring in\n"One Flew Over the Cuckoo\'s Nest".',
                               ]

    # Autobuild the spare part list.
    spare_parts_list = []

    # Open the file to check the data.
    with open("data.csv", "r") as f:
        # Iterate the lines.
        for line in f:
            l = line.strip().split(',')
            # If l in not empty append it to the spare_parts_list.
            if l != ['']:
                spare_parts_list.append(l)

    # Create the global date variable.
    today = datetime.date.today()

    # Create the global mileage variable.
    tries = 0
    while True:
        global_kms = input('\nPlease, provide the current mileage of the vehicle: ')
        if regex_validate_num(global_kms):
            global_kms = int(global_kms)
            break
        else:
            print(error_msg(error_messages, error_messages_advanced, tries))
            tries += 1

    # Create a list to hold all service messages and display them in the end.
    messages = []

    print('\nWhat would you like to do?\n\n'
          'Press "Enter", to run an inspection.\n'
          'Press "1" to update an existing data entry.\n'
          'Press "2" to insert a new data entry.\n'
          'Press "3" to see the existing data entries.\n'
          )
    tries = 0
    while True:
        user_choice = input('\nWaiting for your choice: ')
        # It must be empty (Enter) or a number.
        if user_choice == '':
            # Start the checking procedure.
            # Iterate the lines.
            for x in range(1, len(spare_parts_list)):
                date_changed_insert = spare_parts_list[x][1]
                date_interval_insert = spare_parts_list[x][2]
                kms_changed_insert = spare_parts_list[x][3]
                kms_interval_insert = spare_parts_list[x][4]

                # Check the time that has past since the last change.
                if compare_dates(date_changed_insert, today, date_interval_insert):
                    messages.append(
                        'You have exceeded the allowed {0} months between {1} changes. '
                        'You must change the {1} again now!'.format(
                            (spare_parts_list[x][2].lower()), spare_parts_list[x][0].lower()))

                # Check how many kilometers have past since the last change.
                if compare_kms(global_kms, kms_changed_insert, kms_interval_insert):
                    messages.append(
                        'You have exceeded the allowed {0} kms between {1} changes. '
                        'You must change the {1} again now!'.format(
                            (spare_parts_list[x][4]).lower(), spare_parts_list[x][0].lower()))
            inspection_msg(messages)
            break

        # Update existed data.
        elif user_choice == '1':
            tries = 0
            while True:
                print('\n')
                # Provide the list with the spare parts.
                for x in range(1, (len(spare_parts_list))):
                    print('For {0}, press {1}.'.format(spare_parts_list[x][0], x))
                spare_part_update = input('\nChoose the spare part: ')

                if (spare_part_update != '') and regex_validate_num(spare_part_update):
                    if ((int(spare_part_update)) > len(spare_parts_list)) or (int(spare_part_update) <= 0):
                        print('\n')
                        print(error_msg(error_messages, error_messages_advanced, tries))
                        tries += 1
                    else:
                        break
                else:
                    print(error_msg(error_messages, error_messages_advanced, tries))
                    tries += 1

            tries = 0
            while True:
                date_changed_update = input(
                    '\nPlease, provide the date of the {0} change' \
                    '\n(in ISO 8601 format [YYYY-MM-DD]. E.g. 2016-05-01): '.format(
                        spare_parts_list[(int(spare_part_update))][0].lower()))
                if (date_changed_update != '') and regex_validate_date(date_changed_update):
                    # Check if the date provided is within a logical time span from today.
                    if validate_date(date_changed_update, today) == 1:
                        print(
                            '\nThe date you provided lies ahead in the future.'
                            '\nI cannot accept that, unless you are some king of prophet, or unless you own a time machine.\n')
                    elif validate_date(date_changed_update, today) == -1:
                        print('\nThe date you provided seems too old. I just doesn\'t make sense...\n')
                    else:
                        break
                else:
                    print(error_msg(error_messages, error_messages_advanced, tries))
                    tries += 1

            tries = 0
            while True:
                kms_changed_update = input(
                    '\nPlease, provide the kilometers of the {0} change: '.format(spare_parts_list[
                                                                                      (int(spare_part_update))][
                                                                                      0].lower()))
                if regex_validate_num(kms_changed_update):
                    kms_changed_update = int(kms_changed_update)
                    if kms_changed_update <= global_kms:
                        break
                    else:
                        print(
                            '\nThe kilometers you provided are more than the total kilometers of the vehicle. Something is terribly wrong...\n')
                else:
                    print(error_msg(error_messages, error_messages_advanced, tries))
                    tries += 1

            # Update_entry the data.
            update_entry(spare_parts_list[int(spare_part_update)][0], date_changed_update, kms_changed_update,
                         spare_parts_list)
            break

        # Insert new data entry.
        elif user_choice == '2':
            tries = 0
            while True:
                # Request the spare part.
                spare_part_insert = input('\nPlease provide the name of the spare part: ')
                if regex_validate_string(spare_part_insert):
                    break
                else:
                    print(error_msg(error_messages, error_messages_advanced, tries))
                    tries += 1

            tries = 0
            while True:
                # Request the date of the change.
                date_changed_insert = input('Please provide the date of the last change\n' \
                                            '(in ISO 8601 format [YYYY-MM-DD]. E.g. 2016-05-01): ')
                # It needs work here. The create date object below may need to be changed with the regex above.
                if (date_changed_insert != '') and regex_validate_date(date_changed_insert) and create_date_object(
                        date_changed_insert) and validate_date(date_changed_insert, today):
                    break
                else:
                    print(error_msg(error_messages, error_messages_advanced, tries))
                    tries += 1

            tries = 0
            while True:
                date_interval_insert = input('Please provide the max number of months allowed for the spare part: ')
                if regex_validate_num(date_interval_insert) and int(date_interval_insert) <= 36:
                    break
                else:
                    tries += 1
                    print(error_msg(error_messages, error_messages_advanced, tries))

            tries = 0
            while True:
                kms_changed_insert = input('Please provide the kms of the last change: ')
                if regex_validate_num(kms_changed_insert) and int(kms_changed_insert) < global_kms:
                    while True:
                        if int(kms_changed_insert) < global_kms:
                            break
                        else:
                            print('The kms you provided are more than the current kms of the vehicle.')
                else:
                    tries += 1
                    print(error_msg(error_messages, error_messages_advanced, tries))

            tries = 0
            while True:
                kms_interval_insert = input('Please provide the max kilometers allowed for the spare part: ')
                if regex_validate_num(kms_interval_insert):
                    pass
                    break
                else:
                    tries += 1
                    print(error_msg(error_messages, error_messages_advanced, tries))

            row = [spare_part_insert, date_changed_insert, date_interval_insert, kms_changed_insert,
                   kms_interval_insert]
            spare_parts_list.append(row)
            write_data(spare_parts_list)
            break

        # See existing entries.
        elif user_choice == '3':
            inform(spare_parts_list)
            break
        else:
            print('\n')
            print(error_msg(error_messages, error_messages_advanced, tries))
            tries += 1


if __name__ == '__main__':
    main()

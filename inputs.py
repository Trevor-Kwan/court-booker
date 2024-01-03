from datetime import datetime, timedelta
import json


def venue_list():
    with open("venue.json", 'r') as file:
        data = json.load(file)
    return data


# ask for login details
def login_details_input() -> tuple[str, str]:
    username_input = input("Enter Username Please (Note: caps sensitive) --> ")
    password_input = input("Enter Password Please (Note: caps sensitive) --> ")

    return username_input, password_input


# # ask location to book
def venue_raw_input(venue_data):
    # print venue options
    print("\n Venue Choices:")
    for venue in venue_data:
        id_ = venue['id']
        name = venue['name']
        print(f'\n-> {id_} = {name}')

    # ask venue choice
    print("\nWhich Venue do you Wish to Book? Please Input Corresponding Number.")
    while True:
        try:
            venue_raw_num = int(input("Venue Number --> "))
        # check if input is integer
        except ValueError:
            print("\nSorry, Please Enter a Valid Number ")
        # check if input is between venue number range
        else:
            if venue_raw_num < 1 or venue_raw_num > len(venue_data):
                print("\nSorry, Please Enter a Valid Court Number ")
            else:
                break
    return venue_raw_num


def venue_html_value(venue_num, venue_data):
    for venue in venue_data:
        if venue['id'] == venue_num:
            return venue['html_val']


def court_num_input(venue_num, venue_data):

    # determine range of courts that can be booked
    court_lower, court_upper = -1, -1
    for venue in venue_data:
        if venue['id'] == venue_num:
            court_lower, court_upper = venue['court_range']
            break

    # ask for court choice
    print("\nWhich Court # do you Wish to Book? ")
    while True:
        try:
            court_num = int(input("Court Number --> "))
        # check if input is integer
        except ValueError:
            print("\nSorry, Please Enter a Valid Court Number ")
        # check if input is between court number ranges
        else:
            if court_num > court_upper or court_num < court_lower:
                print("\nSorry, Please Enter a Valid Court Number ")
            else:
                break
    return court_num


def venue_court_input():
    with open("venue.json", 'r') as file:
        venue_data = json.load(file)
    venue_raw_num = venue_raw_input(venue_data)
    venue_html_val = venue_html_value(venue_raw_num, venue_data)
    court_num = str(court_num_input(venue_raw_num, venue_data))
    return venue_html_val, court_num


# ask booking date
def date_raw_input():
    current_dt = datetime.today()
    # ask date
    print("\nWhat Date do you Wish to Book the Court for? ")
    while True:
        # ask for year
        while True:
            try:
                year_input = int(input("Year --> "))
            except ValueError:
                print("\nSorry, Please Enter a Valid Year ")
            else:
                break
        # ask for month
        while True:
            try:
                month_input = int(input("Month (Number)--> "))
            except ValueError:
                print("\nSorry, Please Enter a Valid Month ")
            else:
                break
        # ask for day
        while True:
            try:
                day_input = int(input("Day --> "))
            except ValueError:
                print("\nSorry, Please Enter a Valid Day ")
            else:
                break
        # check if is valid date
        try:
            date = datetime(year_input, month_input, day_input)
        except ValueError:
            print("\nSorry, This is not a Valid Date, Please Enter Again ")
        else:
            if date < current_dt:
                print("\nSorry, This Day Has Passed, Please Enter Again ")
            elif date > current_dt + timedelta(days=3):
                print("\nSorry, Cannot Book For This Day Yet, Please Enter Again ")
            else:
                break
    return year_input, month_input, day_input


def date_input():
    raw_year_input, raw_month_input, raw_day_input = date_raw_input()

    # add necessary string modifications
    if raw_month_input < 10:
        month_input = "0" + f"{raw_month_input}"
    else:
        month_input = f"{raw_month_input}"

    if raw_day_input < 10:
        day_input = "0" + f"{raw_day_input}"
    else:
        day_input = f"{raw_day_input}"

    return '-'.join([f"{raw_year_input}", month_input, day_input])


# ask booking time hour
def hour_raw_input():
    print("\nWhich Timeslot do you Wish to Book? ")
    while True:
        try:
            timeslot_input_raw = input("Starting Hour --> ")
            timeslot_input = int(timeslot_input_raw)
        except ValueError:
            print("\nSorry, Please Enter a Valid Hour Value. ")
        else:
            if timeslot_input > 22 or timeslot_input < 7:
                print("\nSorry, Courts are unavailable during this period. Please Enter Another Hour Value. ")
            elif float(timeslot_input_raw) / timeslot_input != 1:
                print("\nSorry, Please Specify your Hour Value (No Decimals). ")
            else:
                break
    return timeslot_input


def hour_input():
    # return index of html div
    return hour_raw_input() - 6


def target_datetime():
    curr_date = datetime.today()
    return datetime(year=curr_date.year,
                    month=curr_date.month,
                    day=curr_date.day,
                    hour=8,
                    minute=30)

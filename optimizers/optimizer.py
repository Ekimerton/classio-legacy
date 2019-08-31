import itertools
import optimizers.parse_class as parse_class

# Checks if two classes have conflicting ranges, turns out this is a hard problem! (medium more like haha!!!!!! xdddddD)


def is_conflicted(list1, list2):
    for time1 in list1:
        for time2 in list2:
            # If the days are different, they don't overlap for certain
            if time1[:2] == time2[:2]:
                # time1end > time2start AND time2end > time1start, checks if ranges overlap
                if time1[6:] > time2[2:6] and time2[6:] > time1[2:6]:
                    return True
    return False

# Checks to see if a list of times is free during a time, eg between 11301230 for lunch.


def is_free(day_list, start_time, end_time):
    for timeframe in day_list:
        if timeframe[4:] > end_time and start_time > timeframe[:4]:
            return False
    return True

# True means no conflicts, false means there is conflicts


def check_timetable(timetable):
    for i in range(len(timetable)):
        for j in range(i + 1, len(timetable)):
            if is_conflicted(timetable[i], timetable[j]):
                return False
    return True

# Calculates the amount of time in between classes for a day


def calculate_offtime(day):
    offtime = 0
    endh = day[0][:2]
    endm = day[0][2:4]
    for timeframe in day:
        starth = timeframe[:2]
        startm = timeframe[2:4]
        offtime += (int(starth) - int(endh)) + ((int(startm) - int(endm)) / 60)
        endh = timeframe[4:6]
        endm = timeframe[6:]
    return offtime

# Returns all possible permutations


def get_permutations(classes, semester, school):
    resp = parse_class.parse_request(classes, semester, school)
    constant_times = []
    constant_sections = []
    variable_times = []
    variable_sections = []
    for response in resp:
        if response.constant_times:
            for entry in response.constant_times:
                type = entry[0]
                times = entry[1:]
                times = times[0]
                constant_times.append(times)
                constant_sections.append(response.name + ":" + type)
        if response.variable_times:
            for entry in response.variable_times:
                type = entry[0]
                times = entry[1:]
                variable_times.append(times)
                variable_sections.append(response.name + ":" + type)

    ledger = constant_sections + variable_sections
    permutations = []
    for i in list(itertools.product(*variable_times)):
        schedule = constant_times + list(i)
        permutations.append(schedule)
    return ledger, permutations


def flatten_table(timetable):
    flat_list = []
    for sublist in timetable:
        for item in range(1, len(sublist)):
            flat_list.append(sublist[item])
    return flat_list


def addMinutes(time, minutes):
    hour = int(time[:2])
    minute = int(time[2:])
    minute += minutes
    while minute >= 60:
        minute -= 60
        hour += 1
    hour = hour % 24
    hour = str(hour)
    minute = str(minute)
    if len(hour) < 2:
        hour = '0' + hour
    if len(minute) < 2:
        minute = '0' + minute
    return hour + minute


def check_timeframe(timetable, timeframe):
    start_time = timeframe[:4]
    end_time = timeframe[4:]
    free_count = 0
    while addMinutes(start_time, 10) < end_time:
        if is_free(timetable, start_time, addMinutes(start_time, 10)):
            free_count += 1
        else:
            free_count = 0

        if free_count >= 3:
            return True
        start_time = addMinutes(start_time, 10)

    return False

# Things to look for: Lunch free, dinner free, morning/afternoon/evening/mixed, downtime between classes


def analyze_timetable(timetable, params):
    # First flatten
    flat_list = flatten_table(timetable)
    # Sort into lists for Mo, Tu, We, Th, Fr
    day_dict = {'Mo': [], 'Tu': [], 'We': [], 'Th': [], 'Fr': []}
    for time in flat_list:
        day_list = time[:2]
        day_dict[day_list].append(time[2:])
    # Go through lists to analyze time
    time_in_between = 0
    lunch_free = 0
    dinner_free = 0
    day_types = []  # This list is saturated, then the mode becomes the day type
    for day in ['Mo', 'Tu', 'We', 'Th', 'Fr']:
        # Checks only if there are classes that day
        if day_dict[day]:
            day_dict[day].sort()
            # Checks if day is m/a/e/x
            start = int(day_dict[day][0][:4])
            end = int(day_dict[day][len(day_dict[day])-1][4:])
            day_len = end - start
            if day_len > 500:
                day_types.append('x')
            else:
                if start < 1130:
                    day_types.append('m')
                if start >= 1130 and start < 1630:
                    day_types.append('a')
                if start >= 1630:
                    day_types.append('e')
            # Checks if lunch is free
            if check_timeframe(day_dict[day], params['lunch_time']):
                lunch_free += 1
            # Checks if dinner is free
            if check_timeframe(day_dict[day], params['dinner_time']):
                dinner_free += 1
            # Adds total time between classes
            time_in_between += calculate_offtime(day_dict[day])
        else:
            lunch_free += 1
            dinner_free += 1
    day_type = max(set(day_types), key=day_types.count)
    # Score works fine, but I'd like to improve it.
    score = params['offtime']*2*time_in_between + params['lunch'] * \
        5*(5 - lunch_free) + params['dinner']*5*(5 - dinner_free)
    return {'score': score, 'day_type': day_type, 'lunch': lunch_free, 'dinner': dinner_free, 'time_off': round(time_in_between, 2)}


def parse_string(classes, semester, school, score_params):
    ledger, permutations = get_permutations(classes, semester, school)
    valid_list = []
    for i in permutations:
        if check_timetable(i):
            valid_list.append(i)
    return_list = []
    for l in valid_list:
        try:
            return_list.append(
                {'classes': l, 'stats': analyze_timetable(l, score_params)})
        except Exception as e:
            print(e)
    # Sort by score
    return_list = sorted(return_list, key=lambda i: i['stats']['score'])
    return ledger, return_list

# Part for creating a calendar view

# Creates a calender for each timetable


def parse_timetables(timetable_list):
    days_list = []
    for entry in timetable_list:
        days_list.append(create_calendar(entry['classes']))
    return days_list

# TODO Creates a calender for one timetable


def create_calendar(class_list):
    flat_list = [item for sublist in class_list for item in sublist]
    day_list = [[], [], [], [], []]
    day_map = {'Mo': 0, 'Tu': 1, 'We': 2, 'Th': 3, 'Fr': 4}
    for entry in flat_list:
        if len(entry) != 10:
            continue
        if entry[:2] in ['Mo', 'Tu', 'We', 'Th', 'Fr']:
            day_list[day_map[entry[:2]]].append(entry[2:])
    for day in day_list:
        day.sort()
    return day_list

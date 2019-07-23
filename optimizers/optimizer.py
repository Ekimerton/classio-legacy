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
def is_free(day_list, timeset):
    for timeframe in day_list:
        if timeframe[4:] > timeset[:4] and timeset[4:] > timeframe[:4]:
            return False
    return True

# True means no conflicts, false means there is conflicts
def check_timetable(timetable):
    for i in range(len(timetable)):
        for j in range(i + 1, len(timetable)):
            if is_conflicted(timetable[i], timetable[j]):
                return False
    return True

# Calculates the amount of time inbetween classes for a day
def calculate_offtime(day):
    print(day)
    offtime = 0
    end = day[0][:4]
    for timeframe in day:
        start = timeframe[:4]
        print(int(end), int(start))
        offtime += int(start) - int(end)
        end = timeframe[4:]
        print(offtime)
    if offtime % 100 == 0:
        return offtime/100
    elif offtime % 100 == 30:
        return ((offtime - 30)/100) + 0.5
    elif offtime % 100 == 70:
        return ((offtime - 70)/100) + 0.5
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

# Things to look for: Lunch free, dinner free, morning/afternoon/evening/mixed, downtime between classes
def analyze_timetable(timetable):
    #First flatten
    flat_list = [item for sublist in timetable for item in sublist]
    #Sort into lists for Mo, Tu, We, Th, Fr
    day_dict = {'Mo':[], 'Tu':[], 'We':[], 'Th':[], 'Fr':[]}
    for time in flat_list:
        day_list = time[:2]
        day_dict[day_list].append(time[2:])
    # Go through lists to analyze time
    time_in_between = 0
    lunch_free = 0
    dinner_free = 0
    day_types = [] #This list is saturated, then the mode becomes the day type
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
            if is_free(day_dict[day], '11301230') or is_free(day_dict[day], '12301330'):
                lunch_free+=1
            # Checks if dinner is free
            if is_free(day_dict[day], '18301930') or is_free(day_dict[day], '19302030'):
                dinner_free+=1
            # Adds total time between classes
            time_in_between += calculate_offtime(day_dict[day])
    day_type = max(set(day_types), key=day_types.count)
    score = time_in_between + (5 - lunch_free) + (5 - dinner_free)
    return {'score':score, 'day_type':day_type, 'lunch':lunch_free, 'dinner':dinner_free, 'time_off':time_in_between}

def get_score(clas):
    return clas[0]

def parse_string(classes, semester, school):
    ledger, permutations = get_permutations(classes, semester, school)
    valid_list = []
    for i in permutations:
        if check_timetable(i):
            valid_list.append(i)
    return_list = []
    for l in valid_list:
        return_list.append({'classes':l, 'stats':analyze_timetable(l)})

    # Sort by score
    return_list = sorted(return_list, key = lambda i: i['stats']['score'])
    return ledger, return_list

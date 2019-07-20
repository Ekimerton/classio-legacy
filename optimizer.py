import itertools
import parse_class

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

# True means no conflicts, false means there is conflicts
def check_timetable(timetable):
    for i in range(len(timetable)):
        for j in range(i + 1, len(timetable)):
            if is_conflicted(timetable[i], timetable[j]):
                return False
    return True

def get_permutations(classes, semester):
    resp = parse_class.parse_request(classes, semester)
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

ledger, permutations = get_permutations("CISC203,CISC204,CISC220,STAT263,ECON110", 'F')
print(ledger)
valid_list = []

for i in permutations:
    if check_timetable(i):
        valid_list.append(i)

print("Total combos:", str(len(permutations)))
print("Total valid combos:", str(len(valid_list)))

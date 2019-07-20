def hour12to24(timestamp):
    ep_index = timestamp.index(":")
    hour = int(timestamp[:ep_index])
    minute = timestamp[ep_index + 1:ep_index + 3]
    am_pm = timestamp[ep_index + 3:ep_index + 5]
    if hour == 12:
        hour = 0
    if am_pm == "PM":
        hour = str(hour + 12)
    if am_pm == "AM" and hour < 10:
        hour = "0" + str(hour)
    return str(hour) + minute

# TODO: QUEENS DECIDED TO START USING MoTu and such, ruining my parser. Should be easy to fix but BRUH
def standardizeTime(init_time):
    stnd_time = ""
    bits = init_time.split(", ")
    for bit in bits:
        day_string = bit[:2]
        day_list = []
        while day_string in ['Mo', 'Tu', 'We', 'Th', 'Fr']:
             day_list.append(day_string)
             bit = bit[2:]
             day_string = bit[:2]

        first_hour = bit[:bit.index('-')]
        last_hour = bit[bit.index('-') + 1:]
        for day in day_list:
            stnd_time = stnd_time + day + hour12to24(first_hour) + hour12to24(last_hour) + ","
    return stnd_time[:len(stnd_time)-1]

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
            print(timetable[i], timetable[j])
            if is_conflicted(timetable[i], timetable[j]):
                return False
    return True


print(check_timetable([["Mo10301130", "Mo14301530"], ["Mo11301430", "Fr22002300"], ["Mo16001700", "Th10301130"]]))

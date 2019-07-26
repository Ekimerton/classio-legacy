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

def is_free(day_list, timeset):
    for timeframe in day_list:
        if timeframe[4:] > timeset[:4] and timeset[4:] > timeframe[:4]:
            return False
    return True

def calculate_offtime(day):
    offtime = 0
    end = day[0][:4]
    for timeframe in day:
        start = timeframe[:4]
        print(int(end), int(start))
        offtime += int(start) - int(end)
        end = timeframe[4:]
    if offtime % 100 == 0:
        return offtime/100
    elif offtime % 100 == 30:
        return ((offtime - 30)/100) + 0.5
    elif offtime % 100 == 70:
        return ((offtime - 70)/100) + 0.5
    return offtime

'''
def calculate_offtime(day):
    offtime = 0
    end = day[0][:4]
    for timeframe in day:
        offtime += int(timeframe[:4]) - int(end)
        end = timeframe[4:]
    if offtime % 100 == 0:
        return offtime/100
    elif offtime % 100 == 30:
        return ((offtime - 30)/100) + 0.5
    elif offtime % 100 == 70:
        return ((offtime - 70)/100) + 0.5
    return offtime
'''
import optimizers.optimizer as optimizer

ledger, result = optimizer.parse_string("CISC121,CISC124,MATH121", 'F', 'queens')
#result = optimizer.parse_string("CISC221,CISC223,CISC235,CISC271,CLST205", 'W', 'queens'

def tablify(class_list):
    table_lists = []
    for timetable in class_list:
        l = len(timetable['classes'])
        mx = 0
        for cls in timetable['classes']:
            mx = max(mx, len(cls))
        #print(l, mx)
        for i in range(0, mx):
            table_list = [["" for x in range(mx)] for y in range(l)]
            for j in range(0, l):
                try:
                    table_list[j][i] = class_list[i][j]
                except:
                    table_list[j][i] = ""
            table_lists.append(table_list)
        print(table_lists)


print(tablify(result))

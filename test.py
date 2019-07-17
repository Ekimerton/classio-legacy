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

print(hour12to24("12:00AM"))

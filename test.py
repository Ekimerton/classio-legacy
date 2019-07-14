def hour12to24(timestamp):
    ep_index = timestamp.index(":")
    hour = int(timestamp[:ep_index])
    minute = timestamp[ep_index + 1:ep_index + 3]
    am_pm = timestamp[ep_index + 3:ep_index + 5]
    if am_pm == "PM":
        hour = str(hour + 12)
    if am_pm == "AM" and hour < 10:
        hour = "0" + str(hour)
    return str(hour) + minute

def standardizeTime(init_time):
    stnd_time = ""
    bits = init_time.split(", ")
    for bit in bits:
        stnd_time = stnd_time + bit[:2] + hour12to24(bit[3: bit.index('-')]) + hour12to24(bit[bit.index('-') + 2:]) + ","

    return stnd_time[:len(stnd_time)-1]

print(hour12to24("8:00AM"))

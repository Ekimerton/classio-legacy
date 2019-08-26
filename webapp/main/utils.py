def pad_hour(init_hour):
    if init_hour < 10:
        return ('0' + str(init_hour))
    return(str(init_hour))
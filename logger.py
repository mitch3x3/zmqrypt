# LOGGING CODE

def get_user_type():
    print "Enable Logging? (Y/N)"
    log_bool = raw_input('>: ')
    log_bool = str(log_bool).upper()
    if log_bool == 'Y':
        print "Enter log setting: (eg. ALL, INFO, WARNING, ERROR, NONE)"
        type = raw_input('>: ')
        user_type = str(type).upper()
        # Types: INFO, WARNING, ERROR, ALL, NONE
    elif log_bool == 'N':
        user_type = 'NONE'
    else:
        print "You didn't select Y or N"
    return user_type

def log(user_type, log_type, message):
    log_type = str(log_type).upper()
    if user_type != 'NONE':
        if log_type == 'INFO':
            message = 'I: ' + message
        if log_type == 'ERROR':
            message = 'E: ' + message
        if log_type == 'WARNING':
            message = 'W: ' + message
        print message
    elif user_type == 'NONE':
        pass
    else:
        print "INVALID TYPE"

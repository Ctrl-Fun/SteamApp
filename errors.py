import colors

def error(msg:str):

    # Error Message
    return print(f"{colors.boldRed["linestart"]}{msg}{colors.boldRed["lineend"]}\n")
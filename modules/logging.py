import modules.colors as colors

def error(msg:str):
    # Error Message
    return print(f"{colors.boldRed}{msg}{colors.End}\n")

def success(msg:str):
    # Success Message
    return print(f"{colors.Green}{msg}{colors.End}\n")
    
def error(msg:str):
    # ANSI Color code
    RED_BOLD = "\033[1;31m"
    RESET = "\033[0m"

    # Error Message
    return print(f"{RED_BOLD}{msg}{RESET}\n")
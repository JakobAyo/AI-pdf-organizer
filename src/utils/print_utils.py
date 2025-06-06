RED = '\x1b[0;31;40m'
GREEN = '\x1b[0;32;40m'
YELLOW = '\x1b[0;33;40m'
CYAN = '\x1b[0;36;40m'
WHITE = '\x1b[0;30;47m'
ENDC = '\x1b[0m'

def categories(categories):
    for i, category in enumerate(categories):
        print(YELLOW + f"{i + 1}. {category}" + ENDC)

def start():
    size = 30
    return '>'*size + f"{'Processing':^25}" + '<'*size + "\n"


def end():
    size = 30
    return '>'*size + f"{'Done!':^25}" + '<'*size + "\n"

    

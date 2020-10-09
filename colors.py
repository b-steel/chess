class text_colors:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def color(text, color):
    ''' For use with fstring substitution. 
    
    Example usage:
    >>>color('hello', RED)
    >>>'\033[91mhello\033[0m'

    '''
    c = text_colors()
    return getattr(c, color) + text + c.ENDC

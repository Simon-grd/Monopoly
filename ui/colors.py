class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    ORANGE = '\033[38;5;208m'
    GOLD = '\033[38;5;220m'
    LIME = '\033[38;5;118m'
    PINK = '\033[38;5;213m'
    BROWN = '\033[38;5;94m'
    DARK_BLUE = '\033[38;5;21m'
    
    BG_RED = '\033[101m'
    BG_GREEN = '\033[102m'
    BG_YELLOW = '\033[103m'
    BG_BLUE = '\033[104m'
    BG_MAGENTA = '\033[105m'
    BG_CYAN = '\033[106m'
    BG_BLACK = '\033[40m'

class Icons:
    DICE = '🎲'
    MONEY = '💰'
    HOUSE = '🏠'
    HOTEL = '🏨'
    PRISON = '🔒'
    CARD = '🎴'
    ARROW = '➜'
    CHECK = '✓'
    CROSS = '✗'
    STAR = '⭐'
    TROPHY = '🏆'
    PLAYER = '👤'
    ROBOT = '🤖'
    WARNING = '⚠️'
    INFO = 'ℹ️'
    BUILDING = '🏗️'
    BANK = '🏦'
    TRAIN = '🚂'
    ELECTRIC = '⚡'
    WATER = '💧'
    PARKING = '🅿️'
    GO = '▶️'

def colorize(text, color):
    return f"{color}{text}{Colors.RESET}"

def bold(text):
    return f"{Colors.BOLD}{text}{Colors.RESET}"

def dim(text):
    return f"{Colors.DIM}{text}{Colors.RESET}"

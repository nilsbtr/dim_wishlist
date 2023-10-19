class Files:
    SOURCE = 'wishlistRAW.json'
    TARGET = 'wishlist.txt'
    MANIFEST = 'assets/database/manifest.json'
    DIC_WEAPONS = 'assets/dictionary/filtered_weapons.json'
    DIC_PERKS = 'assets/dictionary/filtered_perks.json'


class Colors:  # https://stackoverflow.com/a/39452138
    END = '\33[0m'
    BLACK = '\033[30m'  # Statistics
    RED = '\033[31m'  # HEAD Tag
    GREEN = '\033[32m'  # Successes
    ORANGE = '\033[33m'
    BLUE = '\033[34m'  # DTBS Tag
    PURPLE = '\033[35m'  # Time/Numbers
    CYAN = '\033[36m'  # DICT Tag
    LIGHTGREY = '\033[37m'
    DARKGREY = '\033[90m'
    LIGHTRED = '\033[91m'
    LIGHTGREEN = '\033[92m'
    YELLOW = '\033[93m'  # FILE Tag
    LIGHTBLUE = '\033[94m'
    PINK = '\033[95m'
    LIGHTCYAN = '\033[96m'


class Tags:
    HEAD = f'{Colors.RED}[HEAD]{Colors.END}'
    FILE = f'{Colors.YELLOW}[FILE]{Colors.END}'
    DTBS = f'{Colors.BLUE}[DTBS]{Colors.END}'
    DICT = f'{Colors.CYAN}[DICT]{Colors.END}'

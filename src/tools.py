import os
from datetime import datetime
import shutil

from const import colors, files


def create_backup():  # Creates a backup file inside /backup
    now = datetime.now()
    today = now.strftime("%y%m%d")
    time = now.strftime('/%H%M_')

    path = f'src/backup/{today}'
    if not os.path.exists(path):
        os.makedirs(path)

    with open(files.SOURCE) as source, open(path + time + 'wishlistRAW.txt', 'w') as target:
        for line in source:
            target.write(line)

    with open(files.TARGET) as source, open(path + time + 'wishlist.txt', 'w') as target:
        for line in source:
            target.write(line)

    print(f'{colors.RED}[FILE]{colors.END} Backup created! ({path})')

    path = os.path.dirname(os.path.abspath('main.py')) + '\\src\\backup'
    folders = []

    for root, dirs, filelist in os.walk(path):
        for directory in dirs:
            folders.append(directory)

    if len(folders) > 5:
        folders = list(map(int, folders))
        folders.sort()
        shutil.rmtree(f'src/backup/{folders[0]}')


def create_overview():
    with open('wishlistRAW.txt') as source, open('assets/generated/overview.txt', 'w') as target:
        for line in source:
            if line.startswith('//') or line.startswith('##') or line.startswith('--'):
                target.write(line)


def create_missing():
    weapons = []

    with open('assets/dictonary/dic_weapons.txt', 'r') as file:
        for line in file:
            line = line.split(',')[0]
            weapons.append(line)

    with open('wishlistRAW.txt') as file:
        for line in file:
            if line.startswith('//'):
                weapon = line.split()[1]
                if weapon in weapons:
                    weapons.remove(weapon)

    with open('assets/generated/missing.txt', 'w') as file:
        for weapon in weapons:
            file.write(f'{weapon}\n')


if __name__ == "__main__":
    create_overview()
    create_missing()

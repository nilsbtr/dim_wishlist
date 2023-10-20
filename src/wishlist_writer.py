import json
import os
import shutil
from datetime import date, datetime
from itertools import product

import dictonary_handler as dic
from config import Colors, Files

source: dict


def main():
    global source
    with open(Files.SOURCE) as file:
        source = json.load(file)
    backup()
    header()
    for weapon in source['wishlist']:
        convert_weapon(weapon, source['wishlist'][weapon])


def backup():
    backup_file = f'backup/{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
    shutil.copyfile(Files.TARGET, backup_file)

    content = os.listdir('backup/')

    while len(content) > 5:
        content.sort()
        os.remove(os.path.join('backup/', content.pop(0)))


def header():
    version = source['version']['identifier']
    season = source['version']['identifier'].split('.')[1]
    description = source['version']['description']
    updated = date.today().strftime("%d.%m.%Y")
    with open(Files.TARGET, 'w') as target:
        target.write(f'title: Shaxxs Nightclub Wishlist, Version: {version}\n')
        target.write(
            f'description: Last Updated: {updated} (Season {season}); {description}\n'
        )
        target.write('\n')


def convert_weapon(weapon_name, weapon):  # main writer for all weapons
    for usage in weapon:
        with open(Files.TARGET, 'a') as target:
            target.write('\n')
            target.write(f'// {weapon_name} {usage}\n')
            target.write('\n')
        glob = weapon[usage]['global']
        prefix = create_prefix(weapon_name, usage)

        for roll in weapon[usage]['rolls']:
            process_roll(weapon_name, glob, roll, usage, prefix)


def create_prefix(weapon_name, usage):
    if usage.upper() == 'PVP':
        return f'dimwishlist:item=-{dic.get_hash(weapon_name)}&perks='
    else:
        return f'dimwishlist:item={dic.get_hash(weapon_name)}&perks='


def process_roll(weapon_name, glob, roll, usage, prefix):
    slots = []
    slots.append(to_list(roll.get('masterwork', glob.get('masterwork'))))
    for i in range(1, 5):
        slots.append(to_list(roll.get(f'slot{i}', glob.get(f'slot{i}'))))
    with open(Files.TARGET, 'a') as target:
        slot3 = ', '.join(x for x in slots[3])
        slot4 = ', '.join(x for x in slots[4])
        target.write('// ' + slot3 + ' + ' + slot4 + '\n')
        if slots[0] is not None:
            target.write(f'//notes:{usage}: {", ".join(x for x in slots[0])}\n')
        else:
            target.write(f'//notes:{usage}\n')
    for i in range(1, 5):
        slots[i] = dic.get_perks(weapon_name, i, slots[i])
    convert_roll(slots, prefix)


def to_list(var: str | list[str]) -> list[str]:
    if isinstance(var, str):
        return [var]
    else:
        return var


def convert_roll(slots, prefix):
    with open(Files.TARGET, 'a') as target:
        for slot4 in slots[4]:
            slot4 = [slot4]
            for slot3 in slots[3]:
                slot3 = [slot3]
                for i in range(0, 3):
                    # fmt: off
                    for roll in product(slot4,slot3,*[slots[i] for i in range(2, i, -1)]):
                        target.write(f'{prefix}{",".join(map(str, reversed(roll)))}\n')
                    # fmt: on


def len_source():
    global source
    return len(source['wishlist'])

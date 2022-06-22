from datetime import date

import define as dic
from const import colors, files


def get_version():  # gets the prior version
    with open(files.TARGET) as target:
        title = target.readline()
        if title.startswith('title:'):
            title = title.split()
            i = title.index('Version:')
            return title[i + 1]
        else:
            return 'none'


def clear_target():  # clears the target file
    with open(files.TARGET, 'w') as target:
        print(f'{colors.RED}[FILE]{colors.END}', target.name, 'cleared.')


def write_header():  # writes title and description
    old = get_version()
    version = input(
        f'{colors.VIOLET}[USER]{colors.END} Version {colors.BLACK}({old}){colors.END}: ')
    description = input(
        f'{colors.VIOLET}[USER]{colors.END} Version Description: ')
    updated = date.today().strftime("%d.%m.%Y")
    clear_target()
    with open(files.TARGET, 'a') as target:
        target.write(
            f'title: Shaxxs Nightclub Wishlist, Version: {version}\n')
        target.write(
            f'description: Last Updated: {updated} (Season 17); {description}\n')
        target.write('\n')


def write_section(name):  # writes a new found section
    with open(files.TARGET, 'a') as target:
        target.write('--------------------------------------------------\n')
        target.write(f'##{name}')
        target.write('--------------------------------------------------\n')
        target.write('\n')


def write_weapon(weapon):  # writer for all legendary weapons
    with open(files.TARGET, 'a') as target:
        for wproll in weapon.get_wprolls():
            check_key(weapon.get_name(), weapon.get_name(), dic.weapons)

            target.write(
                f'// {weapon.get_name()} {wproll.get_type()} | {wproll.get_mws()}\n')
            target.write('\n')

            if wproll.get_type() == 'PvP':
                pre = f'dimwishlist:item=-{dic.weapons.get(weapon.get_name())}&perks='
            else:
                pre = f'dimwishlist:item={dic.weapons.get(weapon.get_name())}&perks='

            # rolls[0]: ['TacticalMag FlaredMagwell', 'StatsForAll OneForAll']
            for roll in wproll.get_rolls():
                mags = roll[0].split()
                ltrait, rtrait = roll[1].split()

                check_key(weapon.get_name(), ltrait, dic.traits)
                check_key(weapon.get_name(), rtrait, dic.traits)

                target.write(f'// {ltrait} + {rtrait}\n')
                target.write(create_note(wproll))

                semigr = []  # saves semi god-rolls

                for mag in mags:
                    check_key(weapon.get_name(), mag, dic.suppl)
                    for barrel in wproll.get_barrels():
                        check_key(weapon.get_name(), barrel, dic.suppl)
                        target.write(
                            f'{pre}{create_line(barrel, mag, ltrait, rtrait)}\n')
                    semigr.append(
                        f'{pre}{dic.suppl.get(mag)},{dic.traits.get(ltrait)},{dic.traits.get(rtrait)}\n')
                for line in semigr:
                    target.write(line)
                target.write(
                    f'{pre}{dic.traits.get(ltrait)},{dic.traits.get(rtrait)}\n')
            target.write('\n')


def check_key(weapon, key, dict):  # raising error for non existent key
    if key not in dict:
        print(
            f'{colors.BLUE}[DIC]{colors.END} {key}@{weapon} not found!')
        raise KeyError(f'{key}@{weapon} not found!')


# dimwishlist:item=weapon&perks=barrel,mag,trait_1,trait_2
def create_line(barrel, mag, ltrait, rtrait):  # return the right line format
    return f'{dic.suppl.get(barrel)},{dic.suppl.get(mag)},{dic.traits.get(ltrait)},{dic.traits.get(rtrait)}'


def create_note(wproll):  # creates a note with type and masterwork
    note = f'//notes:{wproll.get_type()}: '
    data = wproll.get_mws().split()
    for mw in data[:-1]:
        note += f'{mw}, '
    note += f'{data[-1]}\n'
    return note


def write_exotic(weapon):  # writer for all exotic weapons
    with open(files.TARGET, 'a') as target:
        for wproll in weapon.get_wprolls():
            check_key(weapon.get_name(), weapon.get_name(), dic.exotics)

            target.write(f'// {weapon.get_name()} {wproll.get_type()}\n')
            target.write('\n')

            if wproll.get_type() == 'PvP':
                pre = f'dimwishlist:item=-{dic.exotics.get(weapon.get_name())}&perks='
            else:
                pre = f'dimwishlist:item={dic.exotics.get(weapon.get_name())}&perks='

            # rolls[0]: ['TacticalMag FlaredMagwell', 'StatsForAll OneForAll']
            for roll in wproll.get_rolls():
                mags = roll[0].split()
                ltrait, rtrait = roll[1].split()

                target.write(f'// {ltrait} + {rtrait}\n')
                target.write(f'//notes:{wproll.get_type()}\n')

                ltrait = check_ekey(weapon.get_name(), ltrait)
                rtrait = check_ekey(weapon.get_name(), rtrait)

                sgr = []  # saves semi god-rolls

                for mag in mags:
                    check_key(weapon.get_name(), mag, dic.suppl)
                    for barrel in wproll.get_barrels():
                        check_key(weapon.get_name(), barrel, dic.suppl)
                        target.write(
                            f'{pre}{dic.suppl.get(barrel)},{dic.suppl.get(mag)},{ltrait},{rtrait}\n')
                    sgr.append(
                        f'{pre}{dic.suppl.get(mag)},{ltrait},{rtrait}\n')
                for line in sgr:
                    target.write(line)
                target.write(f'{pre}{ltrait},{rtrait}\n')
            target.write('\n')


def check_ekey(weapon, key):  # checks if a trait is exotic only otherwise uses normal one
    if key in dic.exotics:
        return dic.exotics.get(key)
    elif key in dic.traits:
        return dic.traits.get(key)
    else:
        print(
            f'{colors.BLUE}[DIC]{colors.END} {key}@{weapon} not found!')
        raise KeyError(f'{key}@{weapon} not found!')

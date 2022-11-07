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
        f'{colors.VIOLET}[USER]{colors.END} Version {colors.BLACK}({old}){colors.END}: '
    )
    description = input(f'{colors.VIOLET}[USER]{colors.END} Version Description: ')
    updated = date.today().strftime("%d.%m.%Y")
    clear_target()
    with open(files.TARGET, 'a') as target:
        target.write(f'title: Shaxxs Nightclub Wishlist, Version: {version}\n')
        target.write(
            f'description: Last Updated: {updated} (Season 17); {description}\n'
        )
        target.write('\n')


def write_section(name):  # writes a new found section
    with open(files.TARGET, 'a') as target:
        target.write('--------------------------------------------------\n')
        target.write(f'##{name}')
        target.write('--------------------------------------------------\n')
        target.write('\n')


def write_weapon(weapon):  # main writer for all weapons
    with open(files.TARGET, 'a') as target:
        wpname = weapon.get_name()
        exotic = wpname in dic.exoticlist
        for wproll in weapon.get_wprolls():
            check_key(wpname, dic.weapons)

            target.write(f'// {wpname} {wproll.get_type()} | {wproll.get_mws()}\n\n')

            pre = create_pre(wpname, wproll.get_type())

            # rolls[0]: ['TacticalMag FlaredMagwell', 'StatsForAll OneForAll']
            for roll in wproll.get_rolls():
                mags = roll[0].split()
                ltrait, rtrait = roll[1].split()

                target.write(f'// {ltrait} + {rtrait}\n')
                target.write(create_note(exotic, wproll))

                ltrait = get_trait(ltrait, exotic)
                rtrait = get_trait(rtrait, exotic)

                semigr = []  # saves semi god-rolls

                for mag in mags:
                    mag = get_value(mag, dic.suppl)
                    for barrel in wproll.get_barrels():
                        barrel = get_value(barrel, dic.suppl)
                        target.write(f'{pre}{barrel},{mag},{ltrait},{rtrait}\n')
                    semigr.append(f'{pre}{mag},{ltrait},{rtrait}\n')
                for line in semigr:
                    target.write(line)
                target.write(f'{pre}{ltrait},{rtrait}\n')
            target.write('\n')


def check_key(key, dict):  # raising error for non existent key
    if key not in dict:
        print(f'{colors.BLUE}[DIC]{colors.END} {key} in {dict} not found!')
        raise KeyError(f'{key} in {dict} not found!')


def get_value(key, dict):  # return value and raises error for non existent key
    if key in dict:
        return dict.get(key)
    else:
        print(f'{colors.BLUE}[DIC]{colors.END} {key} in {dict} not found!')
        raise KeyError(f'{key} in {dict} not found!')


def get_trait(key, exotic):
    # checks if a trait is exotic only otherwise uses normal one
    if exotic and key in dic.exotics:
        return dic.exotics.get(key)
    else:
        return get_value(key, dic.traits)


def create_pre(weapon, type):  # creates the first part of a line
    if type == 'PvP':
        return f'dimwishlist:item=-{dic.weapons.get(weapon)}&perks='
    else:
        return f'dimwishlist:item={dic.weapons.get(weapon)}&perks='


def create_note(exotic, wproll):  # creates a note with type and masterwork
    if exotic:
        return f'//notes:{wproll.get_type()}\n'
    else:
        data = wproll.get_mws().split()
        return f'//notes:{wproll.get_type()}: {", ".join(data)}\n'

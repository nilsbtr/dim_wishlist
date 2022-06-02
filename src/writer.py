from datetime import date

import define as dic
from const import colors, files


# Clears the target file
def clear_target():
    with open(files.TARGET, 'w') as target:
        print(f'{colors.RED}[FILE]{colors.END}', target.name, 'cleared.')


# Writes title and description
def write_header():
    version = input(f'{colors.VIOLET}[USER]{colors.END} Version ... ')
    description = input(f'{colors.VIOLET}[USER]{colors.END} Beschreibung ... ')
    updated = date.today().strftime("%d.%m.%Y")
    with open(files.TARGET, 'a') as target:
        target.write(
            f'title: Shaxxs Nightclub Wishlist, Version: {version}\n')
        target.write(
            f'description: By BelaM, Scythe, PunchedYou; Last Updated: {updated} (Season 17); {description}\n')
        target.write('\n')


def write_section(name):
    with open(files.TARGET, 'a') as target:
        target.write('--------------------------------------------------\n')
        target.write(f'##{name}')
        target.write('--------------------------------------------------\n')
        target.write('\n')


def write_file(weapon):
    with open(files.TARGET, 'a') as target:
        for wproll in weapon.get_wprolls():
            check_key(weapon.get_name(), dic.weapons)

            target.write(
                f'// {weapon.get_name()} {wproll.get_type()} | {wproll.get_mws()}\n')
            target.write('\n')

            # rolls[0]: ['TacticalMag FlaredMagwell', 'StatsForAll OneForAll']
            for roll in wproll.get_rolls():
                mags = roll[0].split()
                ltrait, rtrait = roll[1].split()

                check_key(ltrait, dic.traits)
                check_key(rtrait, dic.traits)

                target.write(f'// {ltrait} + {rtrait}\n')
                target.write(
                    f'//notes:{wproll.get_type()}; Prefered Masterworks: {wproll.get_mws()}\n')

                for mag in mags:
                    check_key(mag, dic.suppl)
                    for barrel in wproll.get_barrels():
                        check_key(barrel, dic.suppl)
                        # dimwishlist:item=weapon&perks=barrel,mag,trait_1,trait_2
                        output = ''

                        if wproll.get_type() == 'PvP':
                            output += 'dimwishlist:item=-'
                        else:
                            output += 'dimwishlist:item='

                        output += f'{dic.weapons.get(weapon.get_name())}&perks='
                        output += f'{dic.suppl.get(barrel)},{dic.suppl.get(mag)},{dic.traits.get(ltrait)},{dic.traits.get(rtrait)}\n'
                        target.write(output)
                if wproll.get_type() == 'PvP':
                    target.write(f'dimwishlist:item=-')
                else:
                    target.write(
                        f'dimwishlist:item={dic.weapons.get(weapon.get_name())}&perks={dic.traits.get(ltrait)},{dic.traits.get(rtrait)}\n')
            target.write('\n')


def check_key(key, dict):  # raising error for non existent key
    if key not in dict:
        raise KeyError(f'{key} not found!')


"""
Weapon:     name => String,
            wprolls => WeaponRoll
WeaponRoll: type => String,
            mws => String,
            barrels => List,
            note => None,
            rolls => List
"""

import re
import time

import define as dic
import objects as obj
import tools
import writer
from const import colors, files


def main():
    # Outputs length to the console
    with open(files.SOURCE) as source:
        source = open(files.SOURCE)
        length = len(source.readlines())
        print(
            f'{colors.RED}[FILE]{colors.END} {source.name} loaded with {length} lines.'
        )

    writer.write_header()  # clears target file and writes header

    start = time.time()

    # looks for all weapons in the file and passes them to grab_data()
    with open(files.SOURCE) as source:
        weapon_counter = 0
        line = source.readline()
        # used while loop to bypass .tell() OSError
        while line:
            if line.startswith('##'):
                writer.write_section(line.strip('#'))
            elif line.startswith('//'):  # finds weapon rolls
                weapon_counter += 1
                weapon_name = line.strip('//').strip()
                source.seek(grab_data(weapon_name, source.tell()))
            line = source.readline()

    end = time.time()

    with open(files.STARRED) as source, open(files.TARGET, 'a') as target:
        for line in source:
            target.write(line)

    tools.create_missing()
    tools.create_overview()

    print(
        f'{colors.RED}[FILE]{colors.END} {colors.GREEN}File successfully converted!{colors.END} {weapon_counter}/{len(dic.weapons)} possible Weapons found.'
    )
    print(
        f'{colors.BLACK}Conversion performed in {colors.VIOLET}{round(end-start, 5)} {colors.BLACK}seconds{colors.END}'
    )


def grab_data(weapon_name, pos):  # saves all data from a weapon into a weapon object
    weapon = obj.Weapon(weapon_name)
    wproll = None
    with open(files.SOURCE) as source:
        source.seek(pos)
        line = source.readline()
        while line:
            if line.startswith('//') or line.startswith('--'):
                break
            elif not line.strip():
                if wproll != None:
                    weapon.append(wproll)
                wproll = None
            elif line.startswith('/'):
                line = line.strip('/').strip()
                header = re.split('\s*[:|]\s*', line)
                wproll = obj.WeaponRoll()
                wproll.set_type(header[0])
                wproll.set_mws(header[1])
                wproll.set_barrels(header[2].split())
            elif line.startswith('Roll: '):
                line = line.replace('Roll: ', '').strip()
                wproll.app_roll(line.split(' | '))
            line = source.readline()
        writer.write_weapon(weapon)
        return (source.tell() - len(line)) - 2


if __name__ == "__main__":
    main()

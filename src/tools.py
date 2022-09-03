def create_overview():
    with open('wishlistRAW.txt') as source, open('docs/overview.txt', 'w') as target:
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

    with open('docs/missing.txt', 'w') as file:
        for weapon in weapons:
            file.write(f'{weapon}\n')


if __name__ == "__main__":
    create_overview()
    create_missing()

from const import colors


def def_dictionary(path):
    dic = {}
    with open(path) as file:
        for line in file:
            if not line.strip() or line.startswith("//"):
                continue
            line = line.strip()
            (key, api) = line.split(",")
            dic[key] = api
        print(
            f'{colors.BLUE}[DIC]{colors.END} Loaded {file.name} with {len(dic)} elements into a dictonary.'
        )
    file.close()
    return dic


def def_register(path):
    register = []
    with open(path) as file:
        for line in file:
            if not line.strip() or line.startswith("//"):
                continue
            line = line.strip()
            register.append(line)
        print(
            f'{colors.YELLOW}[LIST]{colors.END} Registered {file.name} with {len(register)} weapons.'
        )
    file.close()
    return register


weapons = def_dictionary('assets/dictonary/dic_weapons.txt')
suppl = def_dictionary('assets/dictonary/dic_suppl.txt')
traits = def_dictionary('assets/dictonary/dic_traits.txt')
enhanced = def_dictionary('assets/dictonary/dic_enhanced.txt')
exotics = def_dictionary('assets/dictonary/dic_exotics.txt')

craftable = def_register('assets/craftable.txt')
exoticlist = def_register('assets/exotics.txt')

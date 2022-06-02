from const import colors


def def_dictionary(path):
    dic = {}
    with open(path) as file:
        for line in file:
            if not line.strip() or line.startswith("//"):
                continue
            line = line.strip('\n')
            line = line.strip('\t')
            (key, api) = line.split(",")
            dic[key] = api
        print(f'{colors.BLUE}[DIC]{colors.END}', file.name, 'with', len(dic),
              'elements loaded into a dictonary.')
    file.close()
    return dic


def def_craftable():
    craftable = []
    with open('assets/craftable.txt') as file:
        for line in file:
            if not line.strip() or line.startswith("//"):
                continue
            line = line.strip('\n')
            line = line.strip('\t')
            craftable.append(line)
        print(f'{colors.YELLOW}[LIST]{colors.END} Loaded', file.name, 'with',
              len(craftable), 'craftable weapons.')
    file.close()
    return craftable


weapons = def_dictionary('assets/dictonary/dic_weapons.txt')
suppl = def_dictionary('assets/dictonary/dic_suppl.txt')
traits = def_dictionary('assets/dictonary/dic_traits.txt')
enhanced = def_dictionary('assets/dictonary/dic_enhanced.txt')
exotics = def_dictionary('assets/dictonary/dic_exotics.txt')

craftable = def_craftable()

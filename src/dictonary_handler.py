import json

from config import Colors, Files, Tags


weapon_dict: dict
perk_dict: dict

weapon_errors = []
perk_errors = []
roll_errors = []


def load():
    global weapon_dict
    global perk_dict

    weapon_dict = get_json(Files.DIC_WEAPONS)
    perk_dict = get_json(Files.DIC_PERKS)


def get_json(path: str) -> dict:
    with open(path) as file:
        data = json.load(file)
    print(f'{Tags.DICT} Loaded {file.name} with {len(data)} elements.')
    return data


def len_weapons() -> int:
    global weapon_dict
    return len(weapon_dict)


def len_perks() -> int:
    global perk_dict
    return len(perk_dict)


def next_weapon():
    global weapon_dict
    for key in weapon_dict:
        yield key


def next_perk():
    global perk_dict
    for key in perk_dict:
        yield key


def get_weapon(weapon: str) -> dict:
    global weapon_dict
    global weapon_errors

    if wpnobj := weapon_dict.get(weapon):
        return wpnobj
    else:
        if weapon not in weapon_errors:
            weapon_errors.append(weapon)
        return dict()


def is_craftable(weapon: str) -> bool:
    return get_weapon(weapon).get('craftable', False)


def get_hash(weapon: str) -> int | None:
    return get_weapon(weapon).get('hash')


def get_rarity(weapon: str) -> str | None:
    return get_weapon(weapon).get('rarity')


def get_release(weapon: str) -> int | None:
    return get_weapon(weapon).get('release')


def get_socket(weapon: str, slot: int) -> list[int]:
    return get_weapon(weapon).get('sockets', {}).get(f'slot{slot}', [])


def get_source(weapon: str) -> str | None:
    return get_weapon(weapon).get('source')


def get_perks(weapon: str, slot: int, perks: list[str]) -> list[int]:
    global perk_dict
    global perk_errors
    global roll_errors
    result = []

    for perk in perks:
        perk_hash = perk_dict.get(perk, {}).get('hash')
        if not perk_hash:
            if perk not in perk_errors:
                perk_errors.append(perk)
            continue

        if isinstance(perk_hash, list):
            for ph in perk_hash:
                if ph in get_socket(weapon, slot):
                    result.append(ph)
        elif perk_hash in get_socket(weapon, slot):
            result.append(perk_hash)
        else:
            e = f'{perk} ({perk_hash}) on {weapon}'
            if e not in perk_errors:
                perk_errors.append(e)
    return result


def get_type(perk: str) -> str | None:
    return perk_dict.get(perk, {}).get('type')


def out_errors():
    global weapon_errors
    global perk_errors
    global roll_errors

    if len(weapon_errors):
        print(f'The following weapons could not be found {Files.DIC_WEAPONS}:')
        for e in weapon_errors:
            print('   ', e)

    if len(perk_errors):
        print(f'The following perks could not be found in {Files.DIC_PERKS}:')
        for e in perk_errors:
            print('   ', e)

    if len(roll_errors):
        print('The following perks did not fit on a weapon:')
        for e in roll_errors:
            print('   ', e)

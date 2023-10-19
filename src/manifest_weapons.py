import json
import re

import manifest_handler as manifest
from config import Colors, Files

root_node = 3790247699
weapon_type = 3
filtered_weapons = dict()
collected_perks = []


def main():
    global root_node
    global filtered_weapons

    get_weapons(root_node)
    with open(Files.DIC_WEAPONS, 'w') as file:
        json.dump(filtered_weapons, file, indent=2, sort_keys=True)
    print('Weapons done!')
    del filtered_weapons

    filtered_perks = get_perks()
    with open(Files.DIC_PERKS, 'w') as file:
        json.dump(filtered_perks, file, indent=2, sort_keys=True)
    print('Perks done!')


def get_weapons(node_hash: int) -> None:
    global weapon_type

    node = manifest.get_presentation_node(node_hash)

    if node is not None:
        for child in node.get('children', {}).get('presentationNodes', []):
            get_weapons(child.get('presentationNodeHash'))
        for child in node.get('children', {}).get('collectibles', []):
            collectible = manifest.get_collectible(child.get('collectibleHash'))
            item = manifest.get_inventory_item(collectible.get('itemHash'))

            if item is not None:
                versions = item.get('quality', {}).get('versions', [])
                rarity = item.get('inventory', {}).get('tierTypeHash')

                if (
                    item.get('itemType') == weapon_type
                    and 2759499571 in [v.get('powerCapHash') for v in versions]
                    and rarity in [4008398120, 2759499571]
                ):
                    process_weapon(collectible, item)


def process_weapon(collectible, item):
    global filtered_weapons

    fname = format_naming(item['displayProperties']['name'])
    release = manifest.get_release(item)
    craftable = item['inventory'].get('recipeItemHash') is not None

    if item['inventory']['tierTypeHash'] == 2759499571:
        if craftable:
            fname = f'{fname}#C'
            if fname in filtered_weapons:
                return
    elif fname in filtered_weapons:
        if item['hash'] != filtered_weapons[fname].get('hash'):
            dupe_release = filtered_weapons[fname]['release']
            dupe_hash = filtered_weapons[fname]['hash']
            # fmt: off
            if release != dupe_release:
                filtered_weapons[f'{fname}#{dupe_release}'] = filtered_weapons.pop(fname)
                fname = f'{fname}#{release}'
            else:
                filtered_weapons[f"{fname}#{dupe_hash}"] = filtered_weapons.pop(fname)
                fname = f"{fname}#{item['hash']}"
            # fmt: on

    filtered_weapons[fname] = {
        'craftable': item['inventory'].get('recipeItemHash') is not None,
        'hash': item['hash'],
        'rarity': item['inventory']['tierTypeName'],
        'release': release,
        'sockets': get_sockets(item),
        'source': re.sub(
            r"[^\w\s]+", "", collectible['sourceString'].replace('Source: ', '')
        ),
    }


def get_sockets(item):
    socket_entries = item['sockets']['socketEntries'][1:5]
    sockets_obj = dict()

    for i, entry in enumerate(socket_entries, start=1):
        sockets_obj[f'slot{i}'] = process_socket(entry)

    return sockets_obj


def process_socket(entry):
    plug_set_hash = entry.get('randomizedPlugSetHash')
    plug_set_def = manifest.get_plug_set(plug_set_hash)

    perks = []

    if plug_set_def is not None:
        plug_items = plug_set_def.get('reusablePlugItems')

        for plug_item in plug_items:
            perk = plug_item.get('plugItemHash')

            if perk not in perks and collect_perk(perk):
                perks.append(perk)
    else:
        perk = entry.get('singleInitialItemHash')

        if perk not in perks and collect_perk(perk):
            perks.append(perk)
    return perks


def collect_perk(perk):
    global collected_perks

    item = manifest.get_inventory_item(perk)

    if item is not None and item['inventory']['tierType'] != 3:
        if perk not in collected_perks:
            collected_perks.append(perk)
        return True
    else:
        return False


def get_perks():
    global collected_perks

    perks = dict()

    for perk_hash in collected_perks:
        item = manifest.get_inventory_item(perk_hash)

        if item is not None:
            fname = format_naming(item['displayProperties']['name'])

            if 'hash' in perks.get(fname, {}):
                if isinstance(perks.get(fname, {}).get('hash'), list):
                    perks[fname]['hash'].append(perk_hash)
                else:
                    perks[fname]['hash'] = [perks[fname]['hash'], perk_hash]
            else:
                perks.setdefault(fname, {})['hash'] = perk_hash
                perks[fname]['type'] = item['itemTypeDisplayName']
    del collected_perks
    return perks


def format_naming(text):
    text = re.sub(r'[^-()\w\s]+', '', text)
    text.replace('(', '( ')
    text = text.replace('_', ' ').replace('-', ' ').replace('(', '( ')
    return ''.join(t[:1].upper() + t[1:] for t in text.split())


if __name__ == '__main__':
    main()

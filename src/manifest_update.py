import json
import os

import requests

from config import Colors, Files, Tags

base_url = "https://bungie.net"

version = None
local = None
linked_components: dict
target_components = [
    'DestinyCollectibleDefinition',
    'DestinyInventoryItemDefinition',
    'DestinyPlugSetDefinition',
    'DestinyPresentationNodeDefinition',
]


def main():
    global version
    global linked_components

    if (manifest := request_manifest()) is None:
        return

    version = manifest.get('Response', {}).get('version')
    linked_components = (
        manifest.get('Response', {}).get('jsonWorldComponentContentPaths', {}).get('en')
    )

    if check_necessity():
        filtered_components = collect_components()

        if filtered_components is None:
            return

        with open(Files.MANIFEST, 'w') as file:
            json.dump(filtered_components, file)

        print(
            f'{Tags.DTBS} {Colors.GREEN}Succesfully downloaded the database!{Colors.END}\n'
            f'{local} -> {version}'
        )

        import manifest_weapons

        manifest_weapons.main()
    else:
        print(
            f'{Tags.DTBS} The database is already up to date, there is no need to download it again.'
        )


def request_manifest():
    print(f'{Tags.DTBS} Trying to get the manifest...')
    response = requests.get(f'{base_url}/Platform/Destiny2/Manifest/')
    if response.status_code == 200:
        print(
            f'{Tags.DTBS} Succesfully requested manifest. Start updating the database...'
        )
        return response.json()
    else:
        print(
            f'{Tags.DTBS} Error loading the manifest! Try again later.\n'
            f'(The servers are either offline or the rate limit has been exceeded.)'
        )
        return None


def check_necessity():
    global version
    global local

    if not os.path.exists(os.path.join(Files.MANIFEST)):
        return True

    with open(Files.MANIFEST) as file:
        data = json.load(file)

    local = data['version']

    return local != version


def collect_components():
    global version
    global target_components

    filtered_components = {}
    filtered_components['version'] = version

    for component in target_components:
        filtered_components[component] = request_component(component)

        if filtered_components[component] is None:
            return None
    return filtered_components


def request_component(component):
    global linked_components

    url = f'{base_url}{linked_components.get(component)}'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(
            f'{Tags.DTBS} Failed to download component: {component} ({response.status_code})'
        )


if __name__ == '__main__':
    main()

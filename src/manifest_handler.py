import json

import requests

from config import Colors, Files, Tags

manifest: dict

with open(Files.MANIFEST) as file:
    manifest = json.load(file)


def get_collectibles():
    global manifest
    return manifest['DestinyCollectibleDefinition']


def get_collectible(_hash):
    global manifest
    return manifest['DestinyCollectibleDefinition'].get(str(_hash), None)


def get_inventory_items():
    global manifest
    return manifest['DestinyInventoryItemDefinition']


def get_inventory_item(_hash):
    global manifest
    return manifest['DestinyInventoryItemDefinition'].get(str(_hash), None)


def get_presentation_nodes():
    global manifest
    return manifest['DestinyPresentationNodeDefinition']


def get_presentation_node(_hash):
    global manifest
    return manifest['DestinyPresentationNodeDefinition'].get(str(_hash), None)


def get_plug_sets():
    global manifest
    return manifest['DestinyPlugSetDefinition']


def get_plug_set(_hash):
    global manifest
    return manifest['DestinyPlugSetDefinition'].get(str(_hash), None)


response = requests.get(
    'https://raw.githubusercontent.com/DestinyItemManager/d2ai-module/master/watermark-to-season.json'
)
if response.status_code == 200:
    watermark_to_season = response.json()
else:
    watermark_to_season = dict()


def get_release(item):
    global watermark_to_season

    if item.get('iconWatermark') in watermark_to_season:
        return watermark_to_season.get(item.get('iconWatermark'))

import requests
import json

def download_sets():
    r = requests.get('https://api.scryfall.com/sets').json()
    trimmed_sets = {set["code"]: { "name": set["name"], "img_url": set['icon_svg_uri'], "date": set["released_at"]} for set in r['data'] if (set['set_type'] in ['core', 'expansion'])}

    with open('/tmp/data/set-data.json', 'w+') as datafile:
        json.dump(trimmed_sets, datafile)
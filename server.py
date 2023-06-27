from flask import Flask
from os.path import isfile
from os import environ
import requests
import csv

app = Flask(__name__)

@app.route("/")
def health_check():
    return "Live!"

@app.route("/sets", methods=['GET'])
def get_sets():
    try:
        if environ.get("ctt_runtime_evenronment", "NOT_PROVIDED") == "DEV":
            r = requests.get('https://api.scryfall.com/sets').json()
            trimmed_sets = {set["code"]: { "name": set["name"], "img_url": set['icon_svg_uri'], "date": set["released_at"]} for set in r['data'] if (set['set_type'] in ['core', 'expansion'])}
            return trimmed_sets
        else:

    
    except Exception as e:
        err_resp = ("An error occured when trying to get set data: " + str(e), 500)
        return err_resp

@app.route("/cards", methods=['GET'])
def get_cards(): 
    try:
        cards = []
        with open("./data/card_data.csv", 'r') as data_file:
            csvreader = csv.DictReader(data_file)
            for row in csvreader:
                cards.append(row)
        return cards
    
    except Exception as e:
        err_resp = ("An error occured when trying to get card data: " + str(e), 500)
        return err_resp
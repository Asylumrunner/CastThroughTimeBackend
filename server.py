from flask import Flask
from get_sets import download_sets
from os.path import exists
import json

app = Flask(__name__)

@app.route("/")
def health_check():
    return "Live!"

@app.route("/sets", methods=['GET'])
def get_sets():
    file_exists = exists("/data/set-data.json")
    print(file_exists)
        
    if not file_exists:
        print("AAAAAAAAA")
        download_sets()

    with open('./data/set-data.json', 'r') as set_file:
        data = json.load(set_file)
        return data

@app.route("/cards", methods=['GET'])
def get_cards():
    return "TODO: gets the information cards, downloading the file if not available"

@app.route("/refresh", methods=['POST'])
def refresh_data():
    return "TODO: generate the set_data data structure and download the information card file"
import boto3
from os import environ
from botocore.exceptions import ClientError
import csv

def read_cards_file():
    cards = []
    with open("./data/card_data.csv", 'r') as data_file:
        csvreader = csv.DictReader(data_file)
        for row in csvreader:
            cards.append(row)
    return cards
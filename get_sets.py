import requests
import json
import boto3
from os import environ
from botocore.exceptions import ClientError
    
def download_sets_from_scryfall():
    try:
        r = requests.get('https://api.scryfall.com/sets').json()
        trimmed_sets = {set["code"]: { "name": set["name"], "img_url": set['icon_svg_uri'], "date": set["released_at"]} for set in r['data'] if (set['set_type'] in ['core', 'expansion'])}

        s3_client = boto3.client("s3")
        s3_client.put_object(Bucket='castthroughtime', Key='set_data.json', Body=bytes(json.dumps(trimmed_sets).encode('UTF-8')))

        return trimmed_sets
    
    except Exception as e:
        print("Unexpected exception while trying to download data from scryfall")
        raise e
    
def download_sets_from_s3():
    try:
        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket='castthroughtime', Key='set_data.json')
        return json.loads(response["Body"].read())
    except ClientError:
        print("Set data object does not exist, saving client data")
        return download_sets_from_scryfall()
    except Exception as e:
        print("Unexpected exception in downloading sets from S3")
        raise e
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

        bucket_objects = s3_client.list_objects_v2(
            Bucket='castthroughtime',
            Prefix='setsymbol/'
        )

        print(bucket_objects)

        if (bucket_objects['KeyCount'] != 0):
            set_symbols_in_bucket = [object['Key'] for object in bucket_objects['Contents']]
            print(set_symbols_in_bucket)
            missing_sets = [set_code for set_code in trimmed_sets if 'setsymbol/'+ set_code + '.svg' not in set_symbols_in_bucket]
            print(missing_sets)
        else:
            missing_sets = [set_code for set_code in trimmed_sets]
            print(missing_sets)

        for set in missing_sets:
            svg = requests.get(trimmed_sets[set]["img_url"]).text
            s3_client.put_object(
                Bucket='castthroughtime',
                Key='setsymbol/'+set+'.svg',
                ContentType='image/svg+xml',
                ACL='public-read',
                Body=svg
            )

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
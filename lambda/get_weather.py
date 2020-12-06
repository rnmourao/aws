import json
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    my_config = Config(region_name='us-east-1')
    dynamodb = boto3.resource('dynamodb', config=my_config)
    table = dynamodb.Table('weather')    
    
    try:
        city_str = event['city_str'].upper()
        response = table.get_item(Key={'sc': city_str})
        item = response['Item']
        msg = {'city_str': item['sc'], 'temp_int': int(item['t'])}
    except KeyError:
        msg = {'city_str': event['city_str']}
    except ClientError as e:
        msg = {'errorCode': 1, 'errorMessage': e.response['Error']['Message']}
    
    return msg
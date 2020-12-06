import json
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    city_str = event['currentIntent']['slots']['city_str']
    if city_str:
        my_config = Config(region_name='us-east-1')
        dynamodb = boto3.resource('dynamodb', config=my_config)
        table = dynamodb.Table('weather')  
        
        try:
            lookup_name_str = city_str.upper()
            result = table.get_item(Key={'sc': lookup_name_str})
            print('Result:', result)
            item = result['Item']
            response = {
                "sessionAttributes": {
                    "temp_str": int(item['t']),
                    "city_str": city_str
                },
                "dialogAction":{
                    "type": "Close",
                    "fulfillmentState": "Fulfilled",
                    "message": {
                        "contentType": "PlainText",
                        "content": int(item['t'])
                    }
                }
            }       
        except KeyError:
            print("city weather not found for", lookup_name_str)
            response = {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "message": {
                        "contentType": "PlainText",
                        "content": "Please try another city, we couldn't find the weather for that city"
                    },
                    "intentName": "CatWeather",
                    "slots": {
                        "city_str": None
                    },
                    "slotToElicit" : "city_str"
                }
            }
        except ClientError as e:
            raise
    else:
        response = {
            "dialogAction": {
                "type": "ElicitSlot",
                "message": {
                    "contentType": "PlainText",
                    "content": "Name the city your cat lives in, thanks"
                },
                "intentName": "CatWeather",
                "slots": {
                    "city_str": None
                },
                "slotToElicit" : "city_str"
            }
        }
    return response
    
    
# INPUT EXAMPLE:
# {
#   "messageVersion": "1.0",
#   "invocationSource": "DialogCodeHook",
#   "userId": "1012602",
#   "sessionAttributes": {
#   },
#   "bot": {
#     "name": "WeatherCatBot",
#     "alias": "$LATEST",
#     "version": "$LATEST"
#   },
#   "outputDialogMode": "Text",
#   "currentIntent": {
#     "name": "CatWeather",
#     "slots": {
#       "city_str": "CHICAGO"
#     },
#     "confirmationStatus": "None"
#   }
# }
#
# OUTPUT EXAMPLE:
# {
#   "sessionAttributes": {
#     "temp_str": "42",
#     "city_str": "CHICAGO"
#   },
#   "dialogAction": {
#     "type": "Close",
#     "fulfillmentState": "Fulfilled",
#     "message": {
#       "contentType": "PlainText",
#       "content": "42"
#     }
#   }
# }

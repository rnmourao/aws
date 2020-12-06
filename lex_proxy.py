import json
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    USER_ID_STR = event['user_id_str']
    MESSAGE_STR = event['message_str']
    BOT_NAME_STR = "WeatherCatBot"
    BOT_ALIAS_STR = "$LATEST"
    print(USER_ID_STR, MESSAGE_STR)
    my_config = Config(region_name='us-east-1')
    lex = boto3.client('lex-runtime', config=my_config)    
    
    try:
        response = lex.post_text(
            botName=BOT_NAME_STR,
            botAlias=BOT_ALIAS_STR,
            userId=USER_ID_STR,
            inputText=MESSAGE_STR,
            sessionAttributes={}
        )
    except ClientError as e:
        print(e)
        response = "problem with lex"
        
    return response

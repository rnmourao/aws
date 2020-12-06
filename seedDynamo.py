import json
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    my_config = Config(region_name='us-east-1')

    # database    
    dynamodb = boto3.resource('dynamodb', config=my_config)
    table = dynamodb.Table('weather')
    
    with open('cities.csv', 'r') as f:
        lines = f.readlines() 
        for line in lines: 
            sc, t = line.replace('\n', '').split(',')
            try:
                # print(sc, t)
                response = table.put_item(Item={'sc': sc, 't': t})
            except ClientError as e:
                print(sc, e.response['Error']['Code'], e.response['Error']['Message'])
                raise
            
    return True
        
        
# def _get_file(config):
#     # Get cities' data
#     s3client = boto3.client('s3', config=config)
     
#     # These define the bucket and object to read
#     bucketname = '2020-11-25-rnm-website'
#     file_to_read = 'cities.md'
    
#     #Create a file object using the bucket and object key. 
#     fileobj = s3client.get_object(Bucket=bucketname, Key=file_to_read) 
    
#     # open the file object and read it into the variable filedata. 
#     filedata = fileobj['Body'].read()
    
#     # file data will be a binary stream.  We have to decode it 
#     contents = filedata.decode('utf-8')     
    
#     return dict(i.split(',') for i in contents.split('\n'))

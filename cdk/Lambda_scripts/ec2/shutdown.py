import json
from urllib import request
import boto3
import datetime
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

'''
Required information:

body must contain instance id
{
    instanceId: 'asdfasdfaf'   
}
'''

def handler(event, context):
    shutdown_success = False
    request_body = event['body']
    if request_body is None:
        request_body = ''
    
    try:
        instanceID = request_body['instanceID']
    except:
        return {
            'statusCode': '400',
            'body': 'instanceID field missing'
        }

    ec2 = boto3.resource('ec2')
    for i in ec2.instances.all():
        if instanceID == i.id:
            boto3.resource('ec2').Instance(i.id).stop()
            shutdown_success = True
            break
    
    if shutdown_success:
        return {
            'statusCode' : 200,
            'body': json.dumps({
                'result': 'Shutting down ec2 instance: ' + instanceID
            })
        }
    else:
        return {
            'statusCode' : 200,
            'body': json.dumps({
                'result': 'Shutdown failed'
            })
        }
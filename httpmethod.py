from future import print_function
import boto3
import boto
import json

def get_response(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else res,
        'headers': {
            'Content-Type': 'application/json',
        },
    }⁠⁠⁠⁠

def handler(event, context):

    try:
     	table = boto3.resource('dynamodb', region_name='us-west-2').Table('pizzashopmenu')
    except Exception as not_found:
        print("Table doesn't exist.")

    http_method = event['method']
    if http_method == 'GET':
        return get_response(None, table.get_item(Key=event['param']).get('Item'))
    elif http_method == 'POST':        
        return get_response(None, table.put_item(Item=event['body']))
    elif http_method == 'PUT':
        res = table.update_item(
            Key=event['param'],
            UpdateExpression='SET selection = :val1',
            ExpressionAttributeValues={':val1': event['body']['selection']})
        return get_response(None, res)
    elif http_method == 'DELETE':
        return get_response(None, table.delete_item(Key=event['param']))
    else:
        return get_response(ValueError('Unsupported method "{}"'.format(operation)))


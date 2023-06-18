import boto3

def get_signgu_code(signgu_name):
    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
    table = dynamodb.Table('SIGNGU')

    response = table.scan(
        FilterExpression=boto3.dynamodb.conditions.Key('SIGNGU_NM').eq(signgu_name)
    )

    items = response['Items']
    if items:
        return items[0]['SIGNGU_CD']
    else:
        return None


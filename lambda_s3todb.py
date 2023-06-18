import boto3
import csv

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SIGNGU')

def lambda_handler(event, context):
    # 이벤트에서 S3 버킷 이름과 객체 키를 추출
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    
    # S3 객체를 읽어 CSV 파일 파싱
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    rows = response['Body'].read().decode('utf-8').splitlines()
    csv_reader = csv.reader(rows)
    
    # DynamoDB에 데이터 저장
    for row in csv_reader:
        signgu_cd = row[2]
        signgu_nm = row[3]
        
        # DynamoDB 아이템 생성
        item = {
            'SIGNGU_CD': signgu_cd,
            'SIGNGU_NM': signgu_nm
        }
        
        # DynamoDB에 아이템 저장
        table.put_item(Item=item)
    
    return {
        'statusCode': 200,
        'body': 'CSV 파일이 DynamoDB에 저장되었습니다.'
    }

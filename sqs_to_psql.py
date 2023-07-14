import json
import boto3
import psycopg2
import datetime

# Load configuration from config.json file
with open('config.json') as config_file:
    config = json.load(config_file)

# AWS SQS configuration
sqs_endpoint_url = config['sqs_endpoint_url']
sqs_queue_url = config['sqs_queue_url']

# PostgreSQL database configuration
db_host = config['db_host']
db_port = config['db_port']
db_name = config['db_name']
db_user = config['db_user']
db_password = config['db_password']

# Connect to AWS SQS
sqs_client = boto3.client('sqs', endpoint_url=sqs_endpoint_url)

# Establish a connection to the Postgres database
conn = psycopg2.connect(
    host=db_host,
    port=db_port,
    dbname=db_name,
    user=db_user,
    password=db_password
)

# Create a cursor object to execute SQL queries
cursor = conn.cursor()
current_datetime = datetime.date.today()

# masking data device_id and ip with inbuilt hash function in python
def mask_pii(record):
    # Apply masking logic to the 'device_id' and 'ip' fields
    record_body = json.loads(record['body'])
    if 'device_id' in record_body:
        record_body['device_id'] = hash(record_body['device_id'])
    if 'ip' in record_body:
        record_body['ip'] = hash(record_body['ip'])
    record['body'] = json.dumps(record_body)
    return record

# flattening json data received as per our requirement
def flatten_json(record):
    # Flatten the JSON record and return a dictionary
    record_body = json.loads(record['body'])
    flattened_record = {
        'user_id': record_body['user_id'],
        'masked_device_id': record_body.get('device_id'),
        'masked_ip': record_body.get('ip'),
        'device_type':record_body['device_type'],
        'locale':record_body['locale'],
        'app_version':record_body['app_version']
        
    }
    print(flattened_record)
    return flattened_record

# data feeding to postgres user_logins table
def write_to_postgres(record):
    # Insert the record into the Postgres database
    print(record)
    cursor.execute(
        "INSERT INTO user_logins (user_id, masked_ip, masked_device_id, locale, device_type, app_version, create_date) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (record['user_id'], record.get('masked_device_id'), record.get('masked_ip'),record['locale'],record['device_type'],record['app_version'], current_datetime)
    )
    conn.commit()

# migration from sqs to psql when data is received to sqs
def migrate():
    response = sqs_client.receive_message(
            QueueUrl=sqs_queue_url,
            MaxNumberOfMessages=10
        )

    # Process the received messages
    if 'Messages' in response:
        for message in response['Messages']:
            # Retrieve the message body
            message_body = json.loads(message['Body'])
        
            # Process the individual records
            records = message_body['Records']
            for record in records:
                # Apply PII masking to the record
                masked_record = mask_pii(record)
                
                # Flatten the JSON data
                flattened_record = flatten_json(masked_record)
            
                # Write the flattened and masked record to the Postgres database
                write_to_postgres(flattened_record)
            # Delete the received message from the SQS queue
            sqs_client.delete_message(
                QueueUrl=sqs_queue_url,
                ReceiptHandle=message['ReceiptHandle']
            )
    else:
        print("No messages available in the queue.")

# Continuously listen to SQS messages
# while True:
#     migrate()

migrate()
cursor.close()
conn.close()

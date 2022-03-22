import sys
import boto3
import mysql.connector

queue_url = 'https://sqs.us-east-1.amazonaws.com/410439414220/myqueue'
host = 'database-1.cgvs5dpsppxr.us-east-1.rds.amazonaws.com'
user = 'admin'
password = 'admin1234'
database = 'customer'

sqs=boto3.client('sqs')

mydb = mysql.connector.connect(host=host, user=user, password=password, database=database)
mycursor = mydb.cursor()


response = sqs.receive_message(
    QueueUrl=queue_url)

message = response['Messages'][0]

receipt_handle=message['ReceiptHandle']

sqs.delete_message(
    QueueUrl=queue_url,
    ReceiptHandle=receipt_handle
)

print('Received and deleted message: %s' % message["Body"])

customerDetails = message["Body"]
customerDetailsList = customerDetails.split(',')
name = customerDetailsList[0]
country = customerDetailsList[1]
val = (name, country)

sql = "INSERT INTO customers (name, country) VALUES (%s, %s)"

mycursor.execute(sql, val)
mydb.commit()
print("Record inserted in the DB")

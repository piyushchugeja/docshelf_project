import boto3
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Initialize AWS DyanmoDB
dynamodb = boto3.resource('dynamodb', region_name=os.getenv('awsRegion'), aws_access_key_id=os.getenv('accessKeyId'), aws_secret_access_key=os.getenv('awsSecretKey'))

def create_table():
    try:
        table = dynamodb.create_table(
            TableName='DocShelf',
            KeySchema=[
                {
                    'AttributeName': 'email',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'file_name',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'email',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'file_name',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        table.meta.client.get_waiter('table_exists').wait(TableName='DocShelf')
        print("Table created successfully")
        return table
    except Exception as e:
        st.error(f"Error creating table: {e}")
        print(f"Error creating table: {e}")
        return None

def put_item(email, file_name, file_type):
    try:
        table = dynamodb.Table('DocShelf')
        response = table.put_item(
            Item={
                'email': email,
                'file_name': file_name,
                'file_type': file_type
            }
        )
        return True
    except Exception as e:
        st.error(f"Error adding item: {e}")
        return False

def get_items(email):
    try:
        table = dynamodb.Table('DocShelf')
        response = table.query(
            KeyConditionExpression='email = :email',
            ExpressionAttributeValues={
                ':email': email
            }
        )
        items = response['Items']
        item_keys = [item['file_name'] for item in items]
        return item_keys
    except Exception as e:
        st.error(f"Error getting items: {e}")
        return []

def delete_item(email, file_name):
    try:
        table = dynamodb.Table('DocShelf')
        response = table.delete_item(
            Key={
                'email': email,
                'file_name': file_name
            }
        )
        return True
    except Exception as e:
        st.error(f"Error deleting item: {e}")
        return False

# Path: dynamo_operations.py
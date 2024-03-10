import boto3
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Initialize AWS S3 client
s3 = boto3.client('s3', region_name=os.getenv('awsRegion'), aws_access_key_id=os.getenv('accessKeyId'), aws_secret_access_key=os.getenv('awsSecretKey'))
bucket_name = os.getenv('awsBucketName')

def upload_document_to_s3(file):
    try:
        s3.upload_fileobj(file, bucket_name, file.name)
        return True
    except Exception as e:
        st.error(f"Error uploading document: {e}")
        return False

def get_file_from_s3(file_key):
    try:
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        file_content = response['Body'].read()
        file_type = response['ContentType']
        return file_content, file_type
    except Exception as e:
        st.error(f"Error downloading file from S3: {e}")
        return None

def get_url_from_s3(file_key):
    try:
        url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': file_key})
        return url
    except Exception as e:
        st.error(f"Error getting URL from S3: {e}")
        return None

def delete_from_s3(file_key):
    try:
        s3.delete_object(Bucket=bucket_name, Key=file_key)
        return True
    except Exception as e:
        st.error(f"Error deleting file from S3: {e}")
        return False
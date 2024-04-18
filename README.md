# DocShelf

DocShelf is a document storage system built with Python, Streamlit, and AWS services. It allows users to upload, view, and delete documents. The documents are stored in an AWS S3 bucket and the metadata is stored in a DynamoDB table. The application uses AWS Cognito for user authentication.

## Features

- User Authentication with AWS Cognito
- Upload documents to AWS S3
- View list of uploaded documents with download links
- Delete documents from AWS S3 and DynamoDB
- Logout

## Block diagram of system
<img src="https://github.com/piyushchugeja/docshelf_project/assets/66639966/1f67682e-f832-4eca-b592-dfd432fe907d" width="650px"/>


## Installation

1. Clone the repository
2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Usage
1. Set up your AWS credentials and region in the `.streamlit/secrets.toml` file.
```python
awsRegion=<Your AWS Region>
accessKeyId=<Your AWS Access Key ID>
awsSecretKey=<Your AWS Secret Access Key>
userPoolId=<Your AWS Cognito User Pool ID>
appClientId=<Your AWS Cognito App Client ID>
redirectUri=<Your Redirect URI>
awsBucketName=<Your AWS S3 Bucket Name>
```

2. Run the application:

```bash
streamlit run app.py
```

3. Open the application in your web browser.

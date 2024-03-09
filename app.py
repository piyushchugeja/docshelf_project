import streamlit as st
import boto3
import os
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

def list_documents_in_s3():
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        documents = [obj['Key'] for obj in response.get('Contents', [])]
        return documents
    except Exception as e:
        st.error(f"Error listing documents: {e}")
        return []

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

def main():
    st.set_page_config(page_title="DocShelf", page_icon=":file_folder:", layout="wide")
    st.markdown("<head><link rel='stylesheet' href='https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css'><link rel='stylesheet' href='https://pixinvent.com/stack-responsive-bootstrap-4-admin-template/app-assets/fonts/simple-line-icons/style.min.css'></head>", unsafe_allow_html=True)
    st.title("DocShelf - Document Storage System")
    
    icons = {
        'pdf': 'doc',
        'jpg': 'picture',
        'jpeg': 'picture',
        'png': 'picture',
        'doc': 'doc',
        'docx': 'doc',
        'xls': 'doc',
        'xlsx': 'doc',
        'ppt': 'doc',
        'pptx': 'doc',
        'txt': 'notebook',
        'mp4': 'film'
    }
    
    # Sidebar for uploading document
    st.sidebar.title("Upload Document")
    uploaded_file = st.sidebar.file_uploader("Choose a document to upload")

    if uploaded_file is not None:
        if st.sidebar.button("Upload"):
            if upload_document_to_s3(uploaded_file):
                st.sidebar.success("Document uploaded successfully!")
            else:
                st.sidebar.error("Failed to upload document.")

    # Main content area for listing documents
    st.subheader("Uploaded Documents")
    documents = list_documents_in_s3()
    if documents:
        total = len(documents)
        rows = total // 3
        remainder = total % 3
        if remainder > 0:
            rows += 1
        for row in range(rows):
            row_data = "<div class='row my-2'>"
            for col in range(3):
                idx = row * 3 + col
                if idx < total:
                    document = documents[idx]
                    url = get_url_from_s3(document)
                    document_name, document_type = document.split(".")
                    row_data += f"""<div class="col-md-4">
                        <div class="card">
                            <div class="card-content">
                                <div class="card-body">
                                    <div class="media d-flex">
                                        <div class="align-self-center">
                                            <i class="icon-{icons[document_type]} primary h3 float-left"></i> <br>
                                            <span class="badge badge-secondary">{document_type.upper()}</span>
                                        </div>
                                        <div class="media-body text-right">
                                            <h4>{document_name}</h4>
                                            <a href="{url}" target="_blank">
                                                <button class="btn btn-primary btn-sm">Download</button>
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>"""
            row_data += "</div>"
            st.markdown(row_data, unsafe_allow_html=True)
    else:
        st.write("No documents uploaded yet.")

if __name__ == "__main__":
    main()
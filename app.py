import streamlit as st
import boto3
from streamlit_option_menu import option_menu
from tokens import exchange_code_for_token
from s3_operations import *
from dynamo_operations import *

st.set_page_config(page_title="DocShelf", page_icon=":file_folder:", layout="wide", initial_sidebar_state="expanded")
st.markdown("<head><link rel='stylesheet' href='https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css'><link rel='stylesheet' href='https://pixinvent.com/stack-responsive-bootstrap-4-admin-template/app-assets/fonts/simple-line-icons/style.min.css'></head>", unsafe_allow_html=True)

cognito = boto3.client('cognito-idp', region_name=st.secrets['awsRegion'], aws_access_key_id=st.secrets['accessKeyId'], aws_secret_access_key=st.secrets['awsSecretKey'])
user_pool_id = st.secrets['userPoolId']
app_client_id = st.secrets['appClientId']

def render_login():
    login_url = f"https://docshelf.auth.us-east-1.amazoncognito.com/login?response_type=code&client_id={app_client_id}&redirect_uri={st.secrets['redirectUri']}"
    st.header("Login to DocShelf")
    button = """
    <a href="{}">
        <button class="btn btn-primary">Login with Cognito</button>
    </a>
    """.format(login_url)
    st.markdown(button, unsafe_allow_html=True)
    st.stop()

if 'user_info' in st.session_state:
    user_info = st.session_state['user_info']
else:
    if st.query_params and 'code' in st.query_params:
        code = st.query_params['code']
        user_info = exchange_code_for_token(code)
        if user_info:
            st.session_state['user_info'] = user_info
        else:
            st.error("Error exchanging code for tokens. Please try again.")
            render_login()
            st.stop()
    else:
        render_login()
        
def main():
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
        'mp4': 'film',
        'avi': 'film',
        'mkv': 'film',
        'zip': 'folder-alt',
        'rar': 'folder-alt',
        'tar': 'folder-alt',
        'gz': 'folder-alt',
    }

    with st.sidebar:
        st.write(f"Logged in as: {user_info['email']}")
        selected = option_menu("Options",['View', 'Upload', 'Delete'], 
        icons=['eye', 'cloud-upload', 'trash3'], menu_icon="list", default_index=0)
        logout_url = f"https://docshelf.auth.us-east-1.amazoncognito.com/logout?client_id={app_client_id}&logout_uri={st.secrets['redirectUri']}?signout=true"
        logout_button = """
        <a href="{}">
            <button class="btn btn-danger">Logout</button>
        </a>
        """.format(logout_url)
        st.markdown(logout_button, unsafe_allow_html=True)

        
    if selected == 'Upload':
        st.subheader("Upload Document")
        uploaded_file = st.file_uploader("Choose a document to upload")

        if uploaded_file is not None:
            if st.button("Upload"):
                if upload_document_to_s3(uploaded_file) and put_item(user_info['email'], uploaded_file.name, uploaded_file.type):
                    st.success("Document uploaded successfully!")
                else:
                    st.error("Failed to upload document.")
    
    if selected == 'Delete':
        st.subheader("Delete Document")
        documents = get_items(user_info['email'])
        if documents:
            document_to_delete = st.selectbox("Select document to delete", documents)
            if st.button("Delete", type="primary"):
                if delete_from_s3(document_to_delete) and delete_item(user_info['email'], document_to_delete):
                    st.success("Document deleted successfully!")
                else:
                    st.error("Failed to delete document.")
        else:
            st.write("No documents uploaded yet.")
                    
    if selected == 'View':
        st.subheader("Uploaded Documents")
        documents = get_items(user_info['email'])
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
                        if document_type in icons:
                            icon = icons[document_type]
                        else:
                            icon = "notebook"
                        row_data += f"""<div class="col-md-4 col-sm-12">
                            <div class="card">
                                <div class="card-content">
                                    <div class="card-body">
                                        <div class="media d-flex">
                                            <div class="align-self-center">
                                                <i class="icon-{icon} primary h3 float-left text-dark"></i> <br>
                                                <span class="badge badge-secondary">{document_type.upper()}</span>
                                            </div>
                                            <div class="media-body text-right">
                                                <h5 class="text-dark">{document_name}</h5>
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
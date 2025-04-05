from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from firebase_admin import firestore
import os

# Get credential path from environment variable
drive_cred_path = os.getenv("GOOGLE_DRIVE_CREDENTIALS_JSON")

# Initialize Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive.file']
drive_cred = service_account.Credentials.from_service_account_file(
    drive_cred_path, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=drive_cred)

def check_folder_exists(folder_name):
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    folders = results.get('files', [])
    
    if folders:
        return folders[0]['id']
    else:
        return None

def upload_image_to_drive(image_path, destination_name):
    try:
        # Get the images folder ID
        images_folder_id = check_folder_exists("images")
            
        # Prepare the file metadata
        file_metadata = {
            'name': destination_name,
            'parents': [images_folder_id]  # Use the images folder ID
        }
        
        # Prepare the media file
        media = MediaFileUpload(
            image_path,
            mimetype='image/jpeg' if image_path.lower().endswith('.jpg') else 'image/png',
            resumable=True
        )
        
        # Upload the file
        file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink'
        ).execute()
        
        # Make the file publicly accessible
        drive_service.permissions().create(
            fileId=file['id'],
            body={'type': 'anyone', 'role': 'reader'},
            fields='id'
        ).execute()
        
        print(f"Uploaded {image_path} to Google Drive")
        print(f"File ID: {file['id']}")
        print(f"Sharing URL: {file['webViewLink']}")
        
        return {
            'file_id': file['id'],
            'url': file['webViewLink']
        }
    except Exception as e:
        print(f"Error uploading image to Drive: {e}")
        return None 

def get_image(db, image_id):
    try:
        doc_ref = db.collection('images').document(str(image_id))
        doc = doc_ref.get()
        
        if doc.exists:
            return doc.to_dict()
        else:
            print(f"Image with ID {image_id} not found")
            return None
    except Exception as e:
        print(f"Error retrieving image document: {e}")
        return None

def list_images(db, project_name=None, limit=10):
    try:
        query = db.collection('images')
        if project_name:
            query = query.where('project', '==', project_name)
        query = query.order_by('created_at', direction=firestore.Query.DESCENDING).limit(limit)
        docs = query.stream()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        print(f"Error listing images: {e}")
        return []

# Convert DatetimeWithNanoseconds to string before saving
def convert_datetime(obj):
    if hasattr(obj, 'rfc3339'): # Check if it's a DatetimeWithNanoseconds object
        return obj.rfc3339()
    return obj
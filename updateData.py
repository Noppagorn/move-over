import firebase_admin
from firebase_admin import credentials, firestore
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

# Get credential paths from environment variables
firebase_cred_path = os.getenv("FIREBASE_CREDENTIALS_JSON")
drive_cred_path = os.getenv("GOOGLE_DRIVE_CREDENTIALS_JSON")

# Initialize Firebase Admin SDK
firebase_cred = credentials.Certificate(firebase_cred_path)
firebase_admin.initialize_app(firebase_cred)

# Initialize Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive.file']
drive_cred = service_account.Credentials.from_service_account_file(
    drive_cred_path, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=drive_cred)

def check_folder_exists(folder_name):
    """Check if a folder exists in Google Drive and return its ID if found."""
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    folders = results.get('files', [])
    
    if folders:
        return folders[0]['id']
    else:
        return None

def upload_image_to_drive(image_path, destination_name):
    """Upload an image file to Google Drive and return file ID and sharing URL"""
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

def update_image(image_id, update_data):
    """
    Update an existing image document in Firestore and optionally update the image in Drive
    
    Args:
        image_id (str): ID of the image to update
        update_data (dict): Dictionary containing fields to update
            Possible fields:
            - project: project name
            - label: array of labels
            - original_name: new file name
            - image: new image file path (if image needs to be replaced)
            
    Returns:
        bool: True if update was successful, False otherwise
    """
    try:
        db = firestore.client()
        
        # Get the current document
        doc_ref = db.collection('images').document(str(image_id))
        doc = doc_ref.get()
        
        if not doc.exists:
            print(f"Image with ID {image_id} not found")
            return False
            
        current_data = doc.to_dict()
        
        # If a new image is provided, upload it to Drive
        if 'image' in update_data:
            # Get the current file ID
            current_file_id = current_data.get('drive_file_id')
            
            # Upload new image
            destination_name = f"{image_id}_{os.path.basename(update_data['image'])}"
            image_data = upload_image_to_drive(update_data['image'], destination_name)
            
            if not image_data:
                print("Failed to upload new image")
                return False
                
            # Delete old file from Drive
            if current_file_id:
                try:
                    drive_service.files().delete(fileId=current_file_id).execute()
                    print(f"Deleted old file from Drive: {current_file_id}")
                except Exception as e:
                    print(f"Warning: Could not delete old file from Drive: {e}")
            
            # Update the image data
            update_data['image'] = image_data['url']
            update_data['drive_file_id'] = image_data['file_id']
            update_data['original_name'] = os.path.basename(update_data['image'])
        
        # Add updated_at timestamp
        update_data['updated_at'] = firestore.SERVER_TIMESTAMP
        
        # Update the document
        doc_ref.update(update_data)
        print(f"Successfully updated image document with ID: {image_id}")
        
        # Verify the update
        updated_doc = doc_ref.get()
        if updated_doc.exists:
            print(f"Verified update with data: {updated_doc.to_dict()}")
            return True
        else:
            print("Warning: Document not found after update!")
            return False
            
    except Exception as e:
        print(f"Error updating image document: {e}")
        return False

def update_project(project_name, update_data):
    """
    Update all images from a specific project
    
    Args:
        project_name (str): Name of the project to update
        update_data (dict): Dictionary containing fields to update
        
    Returns:
        bool: True if update was successful, False otherwise
    """
    try:
        db = firestore.client()
        
        # Query all documents for the project
        docs = db.collection('images').where('project', '==', project_name).stream()
        
        success = True
        for doc in docs:
            # Update each image
            if not update_image(doc.id, update_data):
                success = False
                print(f"Failed to update image {doc.id} from project {project_name}")
        
        return success
        
    except Exception as e:
        print(f"Error updating project: {e}")
        return False

if __name__ == "__main__":
    # Example usage
    try:
        # Update a single image
        update_data = {
            'project': 'cow',
        }
        update_image("717", update_data)
        
        # Update all images from a project
        # project_update_data = {
        #     'project': 'UpdatedProject'
        # }
        # update_project("Claving", project_update_data)
        
    except Exception as e:
        print(f"Error during update: {e}") 
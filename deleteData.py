import firebase_admin
from firebase_admin import credentials, firestore
from google.oauth2 import service_account
from googleapiclient.discovery import build
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

def delete_image(image_id):
    """
    Delete an image document from Firestore and the corresponding file from Drive
    
    Args:
        image_id (str): ID of the image to delete
        
    Returns:
        bool: True if deletion was successful, False otherwise
    """
    try:
        db = firestore.client()
        
        # Get the document
        doc_ref = db.collection('images').document(str(image_id))
        doc = doc_ref.get()
        
        if not doc.exists:
            print(f"Image with ID {image_id} not found")
            return False
            
        # Get the Drive file ID
        drive_file_id = doc.to_dict().get('drive_file_id')
        
        # Delete the file from Drive if it exists
        if drive_file_id:
            try:
                drive_service.files().delete(fileId=drive_file_id).execute()
                print(f"Deleted file from Drive: {drive_file_id}")
            except Exception as e:
                print(f"Warning: Could not delete file from Drive: {e}")
        
        # Delete the document from Firestore
        doc_ref.delete()
        print(f"Successfully deleted image document with ID: {image_id}")
        
        # Verify the deletion
        deleted_doc = doc_ref.get()
        if not deleted_doc.exists:
            print("Verified document deletion")
            return True
        else:
            print("Warning: Document still exists after deletion!")
            return False
            
    except Exception as e:
        print(f"Error deleting image document: {e}")
        return False

def delete_project(project_name):
    """
    Delete all images from a specific project
    
    Args:
        project_name (str): Name of the project to delete
        
    Returns:
        bool: True if deletion was successful, False otherwise
    """
    try:
        db = firestore.client()
        
        # Query all documents for the project
        docs = db.collection('images').where('project', '==', project_name).stream()
        
        success = True
        for doc in docs:
            # Delete each image
            if not delete_image(doc.id):
                success = False
                print(f"Failed to delete image {doc.id} from project {project_name}")
        
        return success
        
    except Exception as e:
        print(f"Error deleting project: {e}")
        return False

if __name__ == "__main__":
    # Example usage
    try:
        # Delete a single image
        delete_image("1")
        
        # Delete all images from a project
        delete_project("Claving")
        
    except Exception as e:
        print(f"Error during deletion: {e}") 
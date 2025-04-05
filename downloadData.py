from drive_utils import convert_datetime
import firebase_admin
from firebase_admin import credentials, firestore
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import os
import json
from ccmd_logger import Logger

logger = Logger('cows_detector')

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

def check_firebase_connection():
    """Test the connection to Firebase by creating and deleting a test document."""
    try:
        db = firestore.client()
        test_doc = db.collection('test').document('test')
        test_doc.set({'test': 'connection'})
        test_doc.delete()
        logger.info("Successfully connected to Firebase project: cows-detector")
        logger.info("Database connection test passed")
        return True
    except Exception as e:
        logger.error(f"Error connecting to services: {e}")
        logger.error(f"Firebase credentials path: {firebase_cred_path}")
        if not os.path.exists(firebase_cred_path):
            logger.error("Firebase credentials file not found!")
        return False

def download_image(image_url, save_path):
    try:
        # Extract file ID from Google Drive URL if full URL is provided
        if 'drive.google.com' in image_url:
            file_id = image_url.split('/d/')[1].split('/')[0]
        else:
            file_id = image_url
            
        # Get the file content from Google Drive using file ID
        request = drive_service.files().get_media(fileId=file_id)
        
        with open(save_path, 'wb') as f:
            # Download the file in chunks
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
        logger.info(f"Successfully downloaded image to {save_path}")
        return True
    except Exception as e:
        logger.error(f"Error downloading image from Google Drive: {e}")
        return False

def save_metadata(metadata, save_path):
    try:
        with open(save_path, 'w') as f:
            json.dump(metadata, f, indent=2, default=convert_datetime)
        logger.info(f"Successfully saved metadata to {save_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving metadata: {e}")
        return False

def download_image_and_metadata(image_id, output_dir):
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Get image document from Firestore
        db = firestore.client()
        doc_ref = db.collection('images').document(str(image_id))
        doc = doc_ref.get()
        
        if not doc.exists:
            logger.error(f"Image with ID {image_id} not found")
            return False
            
        image_data = doc.to_dict()
        # Download image
        image_url = image_data.get('image')

        if not image_url:
            logger.error(f"No image URL found for image {image_id}")
            return False
            
        image_filename = f"{image_id}_{image_data.get('original_name', 'image.jpg')}"
        image_path = os.path.join(output_dir, image_filename)
        
        if not download_image(image_url, image_path):
            return False
            
        # Save metadata
        metadata_filename = f"{image_id}_metadata.json"
        metadata_path = os.path.join(output_dir, metadata_filename)
        
        if not save_metadata(image_data, metadata_path):
            return False
            
        return True
        
    except Exception as e:
        logger.error(f"Error downloading image and metadata: {e}")
        return False

def download_project_images(project_name, output_dir, limit=None):
    try:
        db = firestore.client()
        # Query all documents for the project using where() instead of filter()
        query = db.collection('images').where('project', '==', project_name).order_by('id', direction=firestore.Query.ASCENDING)
        if limit is not None:
            query = query.limit(limit)
        docs = query.stream()
        logger.info(f"Found documents for project {project_name}" + str(docs))
        success = True
        for doc in docs:
            # Create project-specific directory
            project_dir = os.path.join(output_dir, project_name)
            if not download_image_and_metadata(doc.id, project_dir):
                success = False
                logger.error(f"Failed to download image {doc.id} from project {project_name}")
        
        return success
        
    except Exception as e:
        logger.error(f"Error downloading project: {e}")
        return False

def download_images_by_ids(image_ids, output_dir):
    try:
        success = True
        for image_id in image_ids:
            if not download_image_and_metadata(image_id, output_dir):
                success = False
                logger.error(f"Failed to download image {image_id}")
        return success
    except Exception as e:
        logger.error(f"Error downloading images by IDs: {e}")
        return False

if __name__ == "__main__":
    output_directory = "./downloads"
    if check_firebase_connection():
        try:
            # Example: Download a single image
            # download_image_and_metadata("123", output_directory)
            
            # Example: Download all images from a project
            download_project_images("Claving", output_directory, limit=10)
            
            # Example: Download multiple images by IDs
            # image_ids = ["123", "124", "125"]
            # download_images_by_ids(image_ids, output_directory)
            
            pass
        except Exception as e:
            logger.error(f"Error during processing: {e}") 
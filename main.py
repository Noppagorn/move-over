# Firebase configuration
import firebase_admin # type: ignore
from firebase_admin import credentials, firestore
import os
from termcolor import colored, cprint
from uploadData import process_images_from_uploadgate
from drive_utils import check_folder_exists, upload_image_to_drive
from ccmd_logger import Logger

logger = Logger('cows_detector')

# Get credential path from environment variable
firebase_cred_path = os.getenv("FIREBASE_CREDENTIALS_JSON")

logger.info(f"Using Firebase credentials from: {firebase_cred_path}")
# Initialize Firebase Admin SDK
firebase_cred = credentials.Certificate(firebase_cred_path)
firebase_admin.initialize_app(firebase_cred)

def check_firebase_connection():
    try:
        # Test database connection
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

def check_google_drive_connection():
    try:
        images_folder_id = check_folder_exists("images")
        if images_folder_id:
            logger.info("Successfully connected to Google Drive and verified images folder")
            return True
        else:
            raise Exception("Error: Could access images folder")
    except Exception as e:
        logger.error(f"Error: Could not access Google Drive: {e}")
        return False
    return True

if __name__ == "__main__":
    # Check connections
    if check_firebase_connection() and check_google_drive_connection():
        try:
            db = firestore.client()
            # Example: Upload new images
            # process_images_from_uploadgate(db, "heat", "./uploadGate")
        except Exception as e:
            logger.error(f"Error during processing: {e}")

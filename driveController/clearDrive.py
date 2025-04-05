from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

# Get credential paths from environment variables
drive_cred_path = os.getenv("GOOGLE_DRIVE_CREDENTIALS_JSON")

# Initialize Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive']
drive_cred = service_account.Credentials.from_service_account_file(
    drive_cred_path, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=drive_cred)

def list_all_files():
    """Retrieve all files and folders from Google Drive."""
    query = "trashed = false"
    results = drive_service.files().list(
        q=query, fields="files(id, name, mimeType)").execute()
    return results.get('files', [])

def delete_all_files():
    """Delete all files and folders in Google Drive."""
    files = list_all_files()
    if not files:
        print("No files found in Google Drive.")
        return
    
    for file in files:
        try:
            drive_service.files().delete(fileId=file['id']).execute()
            print(f"Deleted: {file['name']} ({file['id']})")
        except Exception as e:
            print(f"Failed to delete {file['name']}: {e}")

if __name__ == "__main__":
    confirmation = input("Are you sure you want to delete ALL files and folders in Google Drive? (yes/no): ")
    if confirmation.lower() == "yes":
        delete_all_files()
    else:
        print("Operation canceled.")
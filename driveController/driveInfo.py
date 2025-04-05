from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from datetime import datetime

def initialize_drive_service():
    """Initialize and return the Google Drive service."""
    try:
        # Get credential path from environment variables
        drive_cred_path = os.getenv("GOOGLE_DRIVE_CREDENTIALS_JSON")
        if not drive_cred_path:
            raise ValueError("GOOGLE_DRIVE_CREDENTIALS_JSON environment variable is not set")

        # Define required scopes
        SCOPES = [
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive.metadata.readonly'
        ]

        # Create credentials and build service
        credentials = service_account.Credentials.from_service_account_file(
            drive_cred_path, scopes=SCOPES)
        return build('drive', 'v3', credentials=credentials)
    except Exception as e:
        print(f"Error initializing Drive service: {str(e)}")
        return None

def format_bytes(size):
    """Convert bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"

def get_drive_info():
    """Get basic information about the Google Drive account."""
    try:
        # Initialize the service
        service = initialize_drive_service()
        if not service:
            return None

        # Get storage quota information
        about = service.about().get(fields="storageQuota,user").execute()
        if not about:
            print("Failed to get Drive information: Empty response from API")
            return None

        # Extract storage information
        quota = about.get('storageQuota', {})
        total = int(quota.get('total', 0))
        used = int(quota.get('usage', 0))
        used_in_drive = int(quota.get('usageInDrive', 0))
        used_in_trash = int(quota.get('usageInDriveTrash', 0))

        # Extract user information
        user = about.get('user', {})
        
        # Get basic file count
        files = service.files().list(
            fields="files(id, mimeType)",
            pageSize=1000
        ).execute()
        
        file_count = len(files.get('files', []))
        
        # Get basic folder count
        folders = service.files().list(
            q="mimeType='application/vnd.google-apps.folder'",
            fields="files(id)",
            pageSize=1000
        ).execute()
        
        folder_count = len(folders.get('files', []))

        return {
            'storage': {
                'total': format_bytes(total),
                'used': format_bytes(used),
                'used_in_drive': format_bytes(used_in_drive),
                'used_in_trash': format_bytes(used_in_trash),
                'free': format_bytes(total - used),
                'percentage_used': f"{(used/total)*100:.2f}%" if total > 0 else "N/A"
            },
            'user': {
                'email': user.get('emailAddress', 'N/A'),
                'display_name': user.get('displayName', 'N/A')
            },
            'files': {
                'total': file_count
            },
            'folders': {
                'total': folder_count
            }
        }

    except HttpError as error:
        if error.resp.status == 403:
            print("Permission denied. Please check if the service account has the correct permissions.")
        elif error.resp.status == 401:
            print("Authentication failed. Please check your credentials.")
        else:
            print(f"Drive API error: {error}")
        return None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None

def display_drive_info():
    """Display formatted Drive information."""
    info = get_drive_info()
    if not info:
        return
    print(get_drive_info()) 
    print("\n=== Google Drive Account Information ===\n")
    
    # Storage Information
    print("Storage Information:")
    print(f"Total Storage: {info['storage']['total']}")
    print(f"Used Storage: {info['storage']['used']} ({info['storage']['percentage_used']})")
    print(f"Used in Drive: {info['storage']['used_in_drive']}")
    print(f"Used in Trash: {info['storage']['used_in_trash']}")
    print(f"Free Storage: {info['storage']['free']}")
    
    # User Information
    print("\nUser Information:")
    print(f"Email: {info['user']['email']}")
    print(f"Display Name: {info['user']['display_name']}")
    
    # File and Folder Counts
    print("\nFile and Folder Counts:")
    print(f"Total Files: {info['files']['total']}")
    print(f"Total Folders: {info['folders']['total']}")

def main():
    try:
        display_drive_info()
    except Exception as e:
        print(f"Fatal error: {str(e)}")

if __name__ == "__main__":
    main() 
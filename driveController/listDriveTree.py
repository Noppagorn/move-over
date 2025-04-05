from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

# Get credential path from environment variables
drive_cred_path = os.getenv("GOOGLE_DRIVE_CREDENTIALS_JSON")

# Initialize Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive']
drive_cred = service_account.Credentials.from_service_account_file(
    drive_cred_path, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=drive_cred)

def get_drive_files():
    """Retrieve all files and folders from Google Drive."""
    query = "trashed = false"
    results = drive_service.files().list(
        q=query, fields="files(id, name, mimeType, parents)").execute()
    return results.get('files', [])

def build_tree(files):
    """Build a hierarchical tree structure from the file list."""
    tree = {}
    lookup = {}
    
    # Initialize dictionary with file metadata
    for file in files:
        lookup[file['id']] = {
            'name': file['name'],
            'type': 'folder' if file['mimeType'] == 'application/vnd.google-apps.folder' else 'file',
            'children': []
        }
    
    # Organize files into a hierarchy
    for file in files:
        parent_id = file.get('parents', ['root'])[0]  # Default to root if no parent
        if parent_id in lookup:
            lookup[parent_id]['children'].append(lookup[file['id']])
        else:
            tree[file['id']] = lookup[file['id']]  # Root-level items
    
    return tree

def print_tree(node, indent=0):
    """Print the file structure as a tree."""
    print("  " * indent + ("📁 " if node['type'] == 'folder' else "📄 ") + node['name'])
    for child in node['children']:
        print_tree(child, indent + 1)

def display_drive_tree():
    """Retrieve and display the Google Drive tree structure."""
    files = get_drive_files()
    tree = build_tree(files)
    
    print("Google Drive File Structure:")
    for root in tree.values():
        print_tree(root)

if __name__ == "__main__":
    display_drive_tree()

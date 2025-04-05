
import os
import readline
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Get credential paths from environment variables
drive_cred_path = os.getenv("GOOGLE_DRIVE_CREDENTIALS_JSON")

# Initialize Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive']
drive_cred = service_account.Credentials.from_service_account_file(
    drive_cred_path, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=drive_cred)

# Store current directory (root by default)
current_folder_id = "root"

def list_files(folder_id):
    """List all files and folders in the current Google Drive directory."""
    query = f"'{folder_id}' in parents and trashed=false"
    results = drive_service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    files = results.get('files', [])
    
    if not files:
        print("(empty)")
    else:
        for file in files:
            file_type = "📁" if file['mimeType'] == 'application/vnd.google-apps.folder' else "📄"
            print(f"{file_type} {file['name']} ({file['id']})")

def change_directory(folder_name):
    """Change current directory by folder name."""
    global current_folder_id
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    folders = results.get('files', [])
    
    if folders:
        current_folder_id = folders[0]['id']
        print(f"Changed directory to {folder_name}")
    else:
        print(f"Folder '{folder_name}' not found")

def create_folder(folder_name):
    """Create a new folder in the current directory."""
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [current_folder_id]
    }
    folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
    print(f"Created folder: {folder_name} ({folder['id']})")

def delete_file(file_name):
    """Delete a file or folder by name in the current directory."""
    query = f"name='{file_name}' and '{current_folder_id}' in parents and trashed=false"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    
    if files:
        for file in files:
            drive_service.files().delete(fileId=file['id']).execute()
            print(f"Deleted: {file_name} ({file['id']})")
    else:
        print(f"File or folder '{file_name}' not found")

def drive_shell():
    """Interactive shell for Google Drive navigation and commands."""
    global current_folder_id
    print("Google Drive Shell started. Type 'help' for commands.")
    
    while True:
        command = input(f"drive:{current_folder_id}$ ").strip()
        
        if command == "exit":
            break
        elif command == "ls":
            list_files(current_folder_id)
        elif command.startswith("cd "):
            folder_name = command[3:].strip()
            change_directory(folder_name)
        elif command.startswith("mkdir "):
            folder_name = command[6:].strip()
            create_folder(folder_name)
        elif command.startswith("rm "):
            file_name = command[3:].strip()
            delete_file(file_name)
        elif command == "help":
            print("Available commands:")
            print("  ls       - List files in current directory")
            print("  cd <dir> - Change directory")
            print("  mkdir <dir> - Create a new folder")
            print("  rm <file/folder> - Delete a file or folder")
            print("  exit     - Exit the shell")
        else:
            print("Unknown command. Type 'help' for a list of commands.")

if __name__ == "__main__":
    drive_shell()

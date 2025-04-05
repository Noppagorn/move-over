# Main Operations Module

This module handles the core functionality for inserting and retrieving images in the Cows Detector application.

## Functions

### `check_firebase_connection()`
Tests the connection to Firebase by creating and deleting a test document.

```python
def check_firebase_connection():
    """
    Returns:
        bool: True if connection is successful, False otherwise
    """
```

### `check_google_drive_connection()`
Verifies the connection to Google Drive and checks for the existence of the images folder.

```python
def check_google_drive_connection():
    """
    Returns:
        bool: True if connection is successful, False otherwise
    """
```

### `check_folder_exists(folder_name)`
Checks if a folder exists in Google Drive.

```python
def check_folder_exists(folder_name):
    """
    Args:
        folder_name (str): Name of the folder to check
        
    Returns:
        str: Folder ID if found, None otherwise
    """
```

### `upload_image_to_drive(image_path, destination_name)`
Uploads an image file to Google Drive.

```python
def upload_image_to_drive(image_path, destination_name):
    """
    Args:
        image_path (str): Path to the image file
        destination_name (str): Name to save the file as in Drive
        
    Returns:
        dict: Contains 'file_id' and 'url' if successful, None otherwise
    """
```

### `insert_image(db, image_data, image_id, image_name, project_name, labels=None)`
Inserts a new image document into Firestore.

```python
def insert_image(db, image_data, image_id, image_name, project_name, labels=None):
    """
    Args:
        db: Firestore database instance
        image_data (dict): Dictionary containing file_id and url from Google Drive
        image_id (int): Running number ID for the image
        image_name (str): Name of the image file
        project_name (str): Name of the project
        labels (list): List of label/annotation dictionaries (optional)
        
    Returns:
        bool: True if insertion was successful, False otherwise
    """
```

### `get_next_image_id(db)`
Gets the next available running number ID for a new image.

```python
def get_next_image_id(db):
    """
    Args:
        db: Firestore database instance
        
    Returns:
        int: Next available ID, or None if error occurs
    """
```

### `process_images_from_uploadgate(db, project_name, upload_gate_dir="./uploadGate")`
Processes and uploads all images from the uploadGate directory.

```python
def process_images_from_uploadgate(db, project_name, upload_gate_dir="./uploadGate"):
    """
    Args:
        db: Firestore database instance
        project_name (str): Name of the project
        upload_gate_dir (str): Path to uploadGate directory
        
    Returns:
        bool: True if processing was successful, False otherwise
    """
```

### `get_image(db, image_id)`
Retrieves an image document from Firestore.

```python
def get_image(db, image_id):
    """
    Args:
        db: Firestore database instance
        image_id (str): ID of the image to retrieve
        
    Returns:
        dict: Image document data if found, None otherwise
    """
```

### `list_images(db, project_name=None, limit=10)`
Lists images from Firestore with optional filtering.

```python
def list_images(db, project_name=None, limit=10):
    """
    Args:
        db: Firestore database instance
        project_name (str, optional): Filter by project name
        limit (int): Maximum number of documents to return
        
    Returns:
        list: List of image documents
    """
```

## Usage Examples

### Uploading Images

```python
from main import process_images_from_uploadgate

# Upload images from uploadGate directory
db = firestore.client()
process_images_from_uploadgate(db, "ProjectName", "./uploadGate")
```

### Retrieving Images

```python
from main import get_image, list_images

# Get a single image
image_data = get_image(db, "1")

# List images from a project
images = list_images(db, project_name="ProjectName", limit=5)
```

## File Structure

The uploadGate directory should have the following structure:
```
uploadGate/
├── images/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
└── annotations.json
```

### annotations.json Format
```json
{
    "1": {
        "label": [
            {
                "x": 100,
                "y": 100,
                "width": 200,
                "height": 200,
                "rotation": 0,
                "rectanglelabels": ["cow"],
                "original_width": 800,
                "original_height": 600
            }
        ]
    }
}
```

## Error Handling

The module includes comprehensive error handling for:
- File system operations
- Network connectivity issues
- API rate limits
- Invalid file formats
- Database operations
- Missing or invalid data

Each function returns appropriate values to indicate success/failure and includes detailed error logging.

## Logging

The module logs:
- Connection status
- File upload progress
- Database operations
- Error messages
- Operation verification

## Best Practices

1. Always check connection status before operations
2. Use appropriate file formats (jpg, png)
3. Keep file sizes reasonable
4. Handle returned values appropriately
5. Monitor logs for errors
6. Use project names consistently
7. Maintain proper file naming conventions

## Dependencies

- Firebase Admin SDK
- Google Drive API
- Python 3.x
- Required packages:
  ```
  firebase-admin
  google-auth
  google-api-python-client
  ```

## Security Considerations

1. Credentials are managed through environment variables
2. Drive files are set to public read-only access
3. Firebase security rules should be configured
4. Service account permissions are limited

## Performance

- Batch operations for multiple files
- Efficient querying with limits
- Proper indexing on Firestore
- Optimized Drive API usage

## Troubleshooting

Common issues and solutions:
1. Connection errors
   - Check credentials
   - Verify network connectivity
   - Check API quotas

2. File upload issues
   - Verify file permissions
   - Check file size limits
   - Validate file formats

3. Database errors
   - Check Firestore rules
   - Verify document structure
   - Monitor quota limits

For more information about the database module, see the [main README](../README.md). 
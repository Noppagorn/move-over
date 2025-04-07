# Cows Detector Database Library

A Python library for managing image data in Firebase Firestore and Google Drive for the Cows Detector project.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cows-detector.git
cd cows-detector
```

2. Install the package:
```bash
pip install -e .
```

## Setup Requirements

### Firebase Setup
1. Create a Firebase project
2. Generate a service account key (JSON file)
3. Set the environment variable:
```bash
export FIREBASE_CREDENTIALS_JSON="/path/to/your/firebase-credentials.json"
```

### Google Drive Setup
1. Create a Google Cloud Project
2. Enable the Google Drive API
3. Create a service account and download credentials
4. Set the environment variable:
```bash
export GOOGLE_DRIVE_CREDENTIALS_JSON="/path/to/your/drive-credentials.json"
```

## Quick Start

```python
from database.downloadData import (
    download_image_and_metadata,
    download_project_images,
    download_images_by_ids,
    check_firebase_connection
)
from database.drive_utils import (
    upload_image_to_drive,
    get_image,
    list_images
)

# Check Firebase connection
if check_firebase_connection():
    # Download all images from a project (no limit)
    download_project_images(
        project_name="your_project_name",
        output_dir="./downloads"
    )

    # Download limited number of images from a project
    download_project_images(
        project_name="your_project_name",
        output_dir="./downloads",
        limit=10  # Optional: limit to 10 images
    )

    # Download a single image with metadata
    download_image_and_metadata(
        image_id="123",
        output_dir="./downloads"
    )

    # Download multiple images by IDs
    image_ids = ["123", "124", "125"]
    download_images_by_ids(image_ids, "./downloads")

    # Upload an image to Google Drive
    result = upload_image_to_drive(
        image_path="path/to/image.jpg",
        destination_name="image.jpg"
    )

    # Get image details from Firestore
    image_data = get_image("123")

    # List recent images
    recent_images = list_images(project_name="your_project_name", limit=10)
```

## Directory Structure

For bulk uploads, create an `uploadGate` directory with this structure:
```
uploadGate/
├── images/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
└── annotations.json  # optional, for pre-labeled images
```

### Annotations Format (Optional)
```json
{
  "1": {
    "label": ["cow", "calf"]
  },
  "2": {
    "label": ["cow"]
  }
}
```

### Drive Controller Scripts

The `driveController` directory contains utility scripts for managing Google Drive operations:

- `listDriveTree.py`: Lists and displays the hierarchical structure of files and folders in Google Drive
- `clearDrive.py`: Provides functionality to clear or manage content in Google Drive
- `driveInfo.py`: Retrieves and displays information about Google Drive files and folders
- `driveShell.py`: Implements a shell-like interface for Google Drive operations

These scripts use the Google Drive API and require proper authentication setup through service account credentials. They are particularly useful for:
- Visualizing the structure of your Google Drive
- Managing and organizing files in bulk
- Retrieving detailed information about files and folders
- Performing drive operations through an interactive shell interface

## API Reference

### Connection and Setup
- `check_firebase_connection()`: Test the connection to Firebase
- `check_folder_exists(folder_name)`: Check if a folder exists in Google Drive

### Image Operations
- `upload_image_to_drive(image_path, destination_name)`: Upload a single image to Google Drive
- `get_image(db, image_id)`: Retrieve image details from Firestore
- `list_images(db, project_name=None, limit=10)`: List recent images with optional project filter

### Download Operations
- `download_image(image_url, save_path)`: Download a single image from Google Drive
- `download_image_and_metadata(image_id, output_dir)`: Download an image and its metadata
- `download_project_images(project_name, output_dir, limit=None)`: Download all images from a specific project (optionally limited to a specific number)
- `download_images_by_ids(image_ids, output_dir)`: Download multiple images by their IDs

### Utility Functions
- `convert_datetime(obj)`: Convert DatetimeWithNanoseconds to string format
- `save_metadata(metadata, save_path)`: Save metadata to a JSON file

### Data Model

#### Image Document
```python
{
    "id": str,                    # Unique identifier
    "image": str,                 # URL to the image in Google Drive
    "drive_file_id": str,         # Google Drive file ID
    "original_name": str,         # Original filename
    "label": list,                # Array of detection labels
    "project": str,               # Project name
    "created_at": timestamp,      # Creation timestamp
    "updated_at": timestamp       # Last update timestamp
}
```

## Dependencies

- Python >= 3.6
- firebase-admin
- google-api-python-client
- google-auth-httplib2
- google-auth-oauthlib
- termcolor

## Error Handling

The library uses a custom logger (`ccmd_logger`) for consistent error handling and logging:

```python
from ccmd_logger import Logger
logger = Logger('cows_detector')

try:
    download_project_images("project_name", "./downloads")
except Exception as e:
    logger.error(f"Error downloading project: {e}")
```

## Security Considerations

1. Credentials are managed through environment variables
2. Drive files are set to public read-only access
3. Firebase security rules should be configured
4. Service account permissions are limited to file operations

## Troubleshooting

Common issues and solutions:

1. Connection Errors
   - Verify Firebase and Drive credentials paths
   - Check network connectivity
   - Validate API quotas
   - Ensure environment variables are set correctly

2. Upload Issues
   - Check file permissions
   - Verify file size limits
   - Validate file formats
   - Ensure Google Drive folder exists

3. Database Errors
   - Check Firestore rules
   - Verify document structure
   - Monitor quota limits
   - Validate image IDs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
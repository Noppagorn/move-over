# Update Operations Module

This module handles updating images and their metadata in the Cows Detector application, including both Firestore documents and Google Drive files.

## Functions

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

### `update_image(image_id, update_data)`
Updates an existing image document in Firestore and optionally updates the image in Drive.

```python
def update_image(image_id, update_data):
    """
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
```

### `update_project(project_name, update_data)`
Updates all images from a specific project.

```python
def update_project(project_name, update_data):
    """
    Args:
        project_name (str): Name of the project to update
        update_data (dict): Dictionary containing fields to update
        
    Returns:
        bool: True if update was successful, False otherwise
    """
```

## Usage Examples

### Updating a Single Image

```python
from updateData import update_image

# Update image metadata
update_data = {
    'project': 'NewProject',
    'label': [{'x': 100, 'y': 100, 'width': 200, 'height': 200}]
}
update_image("1", update_data)

# Replace image file
update_data = {
    'image': 'path/to/new/image.jpg'
}
update_image("1", update_data)
```

### Updating All Images in a Project

```python
from updateData import update_project

# Update all images in a project
project_update_data = {
    'project': 'UpdatedProject'
}
update_project("Claving", project_update_data)
```

## Update Data Structure

### Image Update Fields

```python
update_data = {
    # Update project name
    'project': 'NewProject',
    
    # Update labels/annotations
    'label': [
        {
            'x': 100,
            'y': 100,
            'width': 200,
            'height': 200,
            'rotation': 0,
            'rectanglelabels': ['cow'],
            'original_width': 800,
            'original_height': 600
        }
    ],
    
    # Update file name
    'original_name': 'new_image.jpg',
    
    # Replace image file
    'image': 'path/to/new/image.jpg'
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
- Drive file operations
- Permission issues

Each function returns appropriate boolean values to indicate success/failure and includes detailed error logging.

## Logging

The module logs:
- Update operations
- File upload progress
- Database operations
- Error messages
- Operation verification
- Drive file operations
- Cleanup operations

## Best Practices

1. Always verify image existence before updating
2. Handle old file cleanup properly
3. Maintain data consistency
4. Use appropriate file formats
5. Keep file sizes reasonable
6. Monitor operation logs
7. Verify updates after completion
8. Handle partial failures gracefully

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
5. File access permissions are managed

## Performance

- Efficient file handling
- Optimized Drive API usage
- Batch operations for project updates
- Proper cleanup of old files
- Minimized API calls

## Troubleshooting

Common issues and solutions:
1. Update failures
   - Check file permissions
   - Verify document existence
   - Check API quotas
   - Validate update data

2. Drive file issues
   - Verify file access
   - Check file size limits
   - Validate file formats
   - Monitor storage quotas

3. Database errors
   - Check Firestore rules
   - Verify document structure
   - Monitor quota limits
   - Check network connectivity

For more information about the database module, see the [main README](../README.md). 
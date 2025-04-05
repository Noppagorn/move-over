# Delete Operations Module

This module handles the deletion of images and their metadata from both Firebase Firestore and Google Drive in the Cows Detector application.

## Functions

### `delete_image(image_id)`
Deletes an image document from Firestore and the corresponding file from Drive.

```python
def delete_image(image_id):
    """
    Args:
        image_id (str): ID of the image to delete
        
    Returns:
        bool: True if deletion was successful, False otherwise
    """
```

### `delete_project(project_name)`
Deletes all images from a specific project.

```python
def delete_project(project_name):
    """
    Args:
        project_name (str): Name of the project to delete
        
    Returns:
        bool: True if deletion was successful, False otherwise
    """
```

## Usage Examples

### Deleting a Single Image

```python
from deleteData import delete_image

# Delete an image
delete_image("1")
```

### Deleting All Images in a Project

```python
from deleteData import delete_project

# Delete all images from a project
delete_project("Claving")
```

## Error Handling

The module includes comprehensive error handling for:
- File system operations
- Network connectivity issues
- API rate limits
- Database operations
- Missing or invalid data
- Drive file operations
- Permission issues
- Concurrent deletion attempts

Each function returns appropriate boolean values to indicate success/failure and includes detailed error logging.

## Logging

The module logs:
- Deletion operations
- Database operations
- Error messages
- Operation verification
- Drive file operations
- Cleanup operations
- Project-level operations

## Best Practices

1. Always verify image existence before deletion
2. Handle Drive file cleanup properly
3. Maintain data consistency
4. Monitor operation logs
5. Verify deletions after completion
6. Handle partial failures gracefully
7. Consider batch operations for large projects
8. Implement proper error recovery

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
2. Drive files are properly cleaned up
3. Firebase security rules should be configured
4. Service account permissions are limited
5. File access permissions are managed
6. Deletion operations are atomic where possible

## Performance

- Efficient file deletion
- Optimized Drive API usage
- Batch operations for project deletion
- Proper cleanup of resources
- Minimized API calls
- Concurrent operation handling

## Data Cleanup

The module ensures:
1. Firestore documents are deleted
2. Drive files are removed
3. Permissions are cleaned up
4. References are updated
5. Storage is freed
6. Metadata is removed

## Troubleshooting

Common issues and solutions:
1. Deletion failures
   - Check file permissions
   - Verify document existence
   - Check API quotas
   - Validate deletion parameters

2. Drive file issues
   - Verify file access
   - Check file ownership
   - Validate file existence
   - Monitor storage quotas

3. Database errors
   - Check Firestore rules
   - Verify document structure
   - Monitor quota limits
   - Check network connectivity

4. Project deletion issues
   - Verify project existence
   - Check for locked files
   - Monitor operation progress
   - Handle partial deletions

## Recovery Procedures

In case of failed deletions:
1. Check operation logs
2. Verify partial deletions
3. Clean up orphaned files
4. Restore if necessary
5. Update metadata
6. Reconcile storage

## Safety Measures

1. Verification before deletion
2. Backup of critical data
3. Atomic operations where possible
4. Rollback capabilities
5. Error recovery procedures
6. Operation logging
7. Status monitoring

## API Limits and Quotas

Consider:
- Drive API quotas
- Firestore limits
- Rate limiting
- Storage quotas
- Operation timeouts
- Concurrent operations

For more information about the database module, see the [main README](../README.md). 
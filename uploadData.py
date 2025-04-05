import os
import json
from firebase_admin import firestore
from termcolor import colored, cprint
from drive_utils import upload_image_to_drive

def get_next_image_id(db):
    try:
        # Query the last document ordered by ID
        docs = db.collection('images').order_by('id', direction=firestore.Query.DESCENDING).limit(1).stream()
        # Get the highest ID and add 1
        for doc in docs:
            return doc.get('id') + 1
        # If no documents exist, start with ID 1
        return 1
    except Exception as e:
        print(f"Error getting next image ID: {e}")
        return None

def insert_image(db, image_data, image_id, image_name, project_name, labels=None):
    # Get current timestamp
    current_time = firestore.SERVER_TIMESTAMP
    
    # Create document data
    doc_data = {
        "image": image_data['url'],
        "drive_file_id": image_data['file_id'],
        "original_name": image_name,
        "id": image_id,
        "label": labels if labels else [],
        "project": project_name,
        "created_at": current_time,
        "updated_at": current_time
    }
    
    try:
        print(f"Attempting to insert document with ID: {image_id}")
        print(f"Document data: {doc_data}")
        # Add document to 'images' collection with image_id as document ID
        db.collection('images').document(str(image_id)).set(doc_data)
        print(f"Successfully inserted image document with ID: {image_id}")
        
        # Verify the document was inserted
        doc_ref = db.collection('images').document(str(image_id)).get()
        if doc_ref.exists:
            print(f"Verified document exists with data: {doc_ref.to_dict()}")
        else:
            print("Warning: Document was not found after insertion!")
        return True
    except Exception as e:
        print(f"Error inserting image document: {e}")
        return False

def process_images_from_uploadgate(db, project_name, upload_gate_dir="./uploadGate"):
    try:
        # Get next available ID
        current_id = get_next_image_id(db)
        if current_id is None:
            raise Exception("Could not get next image ID")
            
        # Get paths to images and annotations directories
        images_dir = os.path.join(upload_gate_dir, "images")
        annotations_file = os.path.join(upload_gate_dir, "annotations.json")
        
        # Ensure images directory exists
        if not os.path.exists(images_dir):
            raise Exception(f"Images directory not found: {images_dir}")
            
        # Load annotations if they exist
        annotations = {}
        if os.path.exists(annotations_file):
            with open(annotations_file, 'r') as f:
                annotations = json.load(f)
        
        # Process each image file
        for image_file in os.listdir(images_dir):
            if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(images_dir, image_file)
                
                # Upload image to Google Drive
                destination_name = f"{current_id}_{image_file}"
                image_data = upload_image_to_drive(image_path, destination_name)
                
                if image_data:
                    # Get labels from annotations if they exist
                    labels = []
                    if str(current_id) in annotations:
                        labels = annotations[str(current_id)].get('label', [])
                    # Insert image document with the Drive data
                    success = insert_image(
                        db=db,
                        image_data=image_data,
                        image_id=current_id,
                        image_name=image_file,
                        project_name=project_name,
                        labels=labels
                    )
                    if success:
                        print(f"Successfully processed {image_file} with ID: {current_id}")
                        current_id += 1
                    else:
                        print(f"Failed to insert image document: {image_file} with ID: {current_id}")
                else:
                    print(f"Failed to upload image to Drive: {image_file} with ID: {current_id}")
        return True
    except Exception as e:
        print(f"Error processing images from uploadGate: {e}")
        return False 
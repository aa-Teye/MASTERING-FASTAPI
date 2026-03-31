import shutil
import os
from fastapi import UploadFile

IMAGE_DIR = "images"

def save_gear_image(file: UploadFile, item_name: str) -> str:
    """
    Takes an uploaded file from FastAPI, safely renames it, 
    saves it to the hard drive, and returns the URL path.
    """
    # Ensure the images folder exists
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
        
    # Clean up the filename so it doesn't break web URLs
    safe_filename = file.filename.replace(" ", "_")
    safe_item_name = item_name.replace(" ", "_")
    
    # Create the final destination path
    file_path = f"{IMAGE_DIR}/{safe_item_name}_{safe_filename}"
    
    # Save the physical image to the disk
    with open(file_path, "wb+") as image_file:
        shutil.copyfileobj(file.file, image_file)
        
    # Return the path so the database can store it
    return f"/{file_path}"
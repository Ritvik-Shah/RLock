import hashlib
import os

def create_database(image_folder_path, database_file_path, unique_device_id):
    # Create or open the database file in append mode
    with open(database_file_path, 'a') as db_file:
        # Iterate over the image files in the specified folder
        for filename in os.listdir(image_folder_path):
            if filename.endswith(('.jpg', '.jpeg', '.png')):  # Filter image files
                # Generate a unique identifier for the image file
                image_identifier = unique_device_id
                # Check the database for repeats
                value = check_database(database_file_path, unique_device_id)
                if (value == True):
                    return value
                # Write the unique identifier and image file name to the database file
                db_file.write(f"{image_identifier} {filename}\n")
    return False


def check_database(database_file_path, unique_device_id):
    # Read the database file
    with open(database_file_path, 'r') as file:
        # Iterate over each line in the file
        for line in file:
            # Split the line into identifier and filename
            identifier, filename = line.strip().split(' ')
            # Checks if anyone had been registered on the device before
            if identifier == unique_device_id:
                return True
    return False
    

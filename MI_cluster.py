#!/usr/bin/env python3

import os
import shutil
import zipfile

def extract_zip(zip_file, extract_dir):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    return os.path.splitext(os.path.basename(zip_file))[0]

def create_folder_clones(zip_file, cloning_number):
    # Check if the zip file exists
    if not os.path.isfile(zip_file):
        print(f"Error: File '{zip_file}' does not exist!")
        return

    # Check if cloning_number is a positive integer
    try:
        cloning_number = int(cloning_number)
        if cloning_number <= 0:
            raise ValueError
    except ValueError:
        print("Error: Cloning number must be a positive integer!")
        return

    # Extract the zip file
    extracted_folder = extract_zip(zip_file, '.')

    # Get the directory where the zip file is located
    zip_dir = os.path.dirname(os.path.abspath(zip_file))

    # Create clones
    for i in range(1, cloning_number + 1):
        clone_folder = os.path.join(zip_dir, f"{extracted_folder}_clone_{i}")
        shutil.copytree(extracted_folder, clone_folder)
        print(f"Clone {i} created: {clone_folder}")

    # Delete the extracted folder
    shutil.rmtree(extracted_folder)

if __name__ == "__main__":
    # Prompt the user for zip file name and cloning number
    zip_file = input("Enter zip file name: ")
    cloning_number = input("Enter cloning number: ")

    create_folder_clones(zip_file, cloning_number)

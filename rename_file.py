import os
import re
import shutil

# Define the folder path
folder_path = './A'  # Replace with the path to your folder

# Define the regex pattern to match the files
pattern = re.compile(r'(.+_+\d+)\.png')

# Iterate over all files in the folder
for filename in os.listdir(folder_path):
    match = pattern.match(filename)
    if match:
        # Extract the base name (without the .png extension)
        base_name = match.group(1)
        # Create the new file name
        new_filename = f'{base_name}_test.png'
        # Construct the full file paths
        old_file = os.path.join(folder_path, filename)
        new_file = os.path.join(folder_path, new_filename)
        # Copy the file and add _test to the copied file name
        shutil.copy2(old_file, new_file)
        print(f'Copied: {filename} -> {new_filename}')

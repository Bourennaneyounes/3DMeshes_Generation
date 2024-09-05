import shutil
import os
import glob
import re  # Import regex module

# Define source and destination directories
source_dir = './A/'
dest_dir_black = './ZITS_inpainting/masks'  
dest_dir_apple = './ZITS_inpainting/images'  

# Ensure destination directories exist
os.makedirs(dest_dir_black, exist_ok=True)
os.makedirs(dest_dir_apple, exist_ok=True)

# Define file patterns
file_pattern_black = os.path.join(source_dir, '*_filter_orange_gray_black.png')
file_pattern_apple = os.path.join(source_dir, '*_test.png')

# Find all files matching the patterns
files_to_copy_black = glob.glob(file_pattern_black)

# Define a regex pattern for apple_*.png where * is an integer
# integer_pattern = re.compile(r'apple_\d+\.png')

# Filter files matching apple_*.png where * is an integer
# files_to_copy_apple = [f for f in glob.glob(file_pattern_apple) if integer_pattern.match(os.path.basename(f))]
files_to_copy_apple = glob.glob(file_pattern_apple)
# Function to copy files to the destination directory
def copy_files(files, dest_dir):
    for file_path in files:
        # Extract the file name from the path
        file_name = os.path.basename(file_path)
        
        # Define the destination file path
        dest_file_path = os.path.join(dest_dir, file_name)
        
        # Copy the file
        shutil.copy(file_path, dest_file_path)
        print(f'Copied {file_name} to {dest_dir}')

# Copy the files
copy_files(files_to_copy_black, dest_dir_black)
copy_files(files_to_copy_apple, dest_dir_apple)

print('File copying completed.')

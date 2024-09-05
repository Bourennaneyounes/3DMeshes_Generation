import os
import subprocess

# Define the paths
img_dir = './images/'
mask_dir = './masks/'
ckpt_path = './ckpt'
config_file = './config_list/config_ZITS_HR_places2.yml'
gpu_ids = '0'
save_path = './output'

# List all image files in the image directory
img_files = sorted([f for f in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir, f))])
mask_files = sorted([f for f in os.listdir(mask_dir) if os.path.isfile(os.path.join(mask_dir, f))])

# Ensure there is a matching mask for each image
if len(img_files) != len(mask_files):
    print("Error: The number of images and masks do not match.")
    exit(1)

# Iterate over the image files and run the command for each pair
for img_file, mask_file in zip(img_files, mask_files):
    img_path = os.path.join(img_dir, img_file)
    mask_path = os.path.join(mask_dir, mask_file)
    
    command = f"python single_image_test.py --path {ckpt_path} --config_file {config_file} --GPU_ids '{gpu_ids}' --img_path {img_path} --mask_path {mask_path} --save_path {save_path}"
    
    # Run the command
    print(f"Running command: {command}")
    subprocess.run(command, shell=True)

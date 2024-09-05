import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def replace_with_original(original_image_path, inpainted_image_path, mask_image_path, output_image_path):
    # Load images
    original_img = cv2.imread(original_image_path)
    inpainted_img = cv2.imread(inpainted_image_path)
    mask = cv2.imread(mask_image_path, cv2.IMREAD_GRAYSCALE)  # Mask should be in grayscale

    # Check if images have been loaded correctly
    if original_img is None or inpainted_img is None or mask is None:
        print(f"Error loading images for {original_image_path}, {inpainted_image_path}, or {mask_image_path}.")
        return

    # Ensure all images have the same dimensions
    if original_img.shape != inpainted_img.shape or original_img.shape[:2] != mask.shape:
        print(f"Images and mask dimensions do not match for {original_image_path}, {inpainted_image_path}, or {mask_image_path}.")
        return

    # Convert mask to binary (0 or 255) if it's not already
    _, binary_mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

    # Replace regions in the inpainted image with regions from the original image using the mask
    # Convert mask to 3 channels to match the original image
    binary_mask_colored = cv2.cvtColor(binary_mask, cv2.COLOR_GRAY2BGR)
    
    # Apply mask to original image and inpainted image
    region_from_original = cv2.bitwise_and(original_img, binary_mask_colored)
    region_from_inpainted = cv2.bitwise_and(inpainted_img, cv2.bitwise_not(binary_mask_colored))

    # Combine the two regions
    modified_img = cv2.add(region_from_original, region_from_inpainted)

    # Save the output image
    cv2.imwrite(output_image_path, modified_img)
    print(f"Modified image saved as {output_image_path}")

    # Convert images from BGR to RGB for matplotlib
    original_img_rgb = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
    inpainted_img_rgb = cv2.cvtColor(inpainted_img, cv2.COLOR_BGR2RGB)
    modified_img_rgb = cv2.cvtColor(modified_img, cv2.COLOR_BGR2RGB)

    
# Define input and output directories
input_dir_original = './A/'
input_dir_inpainted = '/home/ybourennane/fixTex/ZITS_inpainting/output/'
input_dir_mask = './A/'
output_dir = '/home/ybourennane/blenderProc/BlenderProc/blenderproc/scripts/output'

# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# List all original image files in the input directory
original_files = sorted([f for f in os.listdir(input_dir_inpainted) if f.endswith('.png')])

# Process each file
for original_file in original_files:
    inpainted_file = original_file
    base_name = original_file.replace('_test.png', '')
    
    mask_file = f"{base_name}_filtered_out_mask.png"
    output_file = f"{base_name}.png"

    original_path = os.path.join(input_dir_original, original_file)
    inpainted_path = os.path.join(input_dir_inpainted, inpainted_file)
    mask_path = os.path.join(input_dir_mask, mask_file)
    output_path = os.path.join(output_dir, output_file)

    replace_with_original(original_path, inpainted_path, mask_path, output_path)

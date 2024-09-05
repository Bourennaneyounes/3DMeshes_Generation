# Generation of 3D Meshes Dataset

## Description

This project focuses on generating and utilizing 3D meshes, particularly of fruits and vegetables. It is divided into two main stages:

1. **Generation of 3D Meshes**: Creating detailed 3D meshes of various fruits and vegetables.
2. **Simulation and Dataset Creation**: Using the generated meshes to simulate scenes with BlenderProc and create datasets, such as NOCS CAMERA.

## Prerequisites

Ensure you have the following installed:

- **Ubuntu**: The project is tested on Ubuntu.
- **Stable Diffusion 3**: For generating high-quality datasets of images.
- **Instant Meshes**: For converting images into 3D meshes.
- **Blender**: Needed for refining 3D meshes.
- **BlenderProc**: To simulate scenes and create the final datasets.

## Pipeline Overview

The project pipeline is divided into two main stages:
1. **Image Generation**: Using Stable Diffusion to generate a large dataset of images.
2. **3D Mesh Generation and Simulation**: Converting the images into 3D meshes and simulating scenes with BlenderProc.

## Detailed Steps

### Step 1: Generating a Dataset of Images using Stable Diffusion 3

1. **Create a Virtual Environment**:
   ```bash
   python -m venv myenv
   source myenv/bin/activate
   ```

2. **Install Required Packages**:
   ```bash
   pip install diffusers torch transformers ipywidgets accelerate protobuf sentencepiece
   ```

3. **Prepare Directories**:
   - Create a folder to store the generated images and update the path in the `image_generation.py` script accordingly.

4. **Run Image Generation Script**:
   ```bash
   python image_generation.py
   ```
   In this project, 10,000 images were generated for 50 categories of fruits using the `stabilityai/stable-diffusion-3-medium-diffusers` model.

### Step 2: Generating 3D Meshes with Instant Meshes

1. **Install Instant Meshes**:
   Follow the [installation guide](https://github.com/TencentARC/InstantMesh) to install Instant Meshes.

2. **Run Instant Meshes**:
   ```bash
   python run.py configs/instant-mesh-large.yaml path_to_your_saved_images --save_video --export_texmap
   ```
   Replace `path_to_your_saved_images` with the folder where your generated images are stored. This will generate the 3D meshes along with texture maps.

3. **Important**:
   - The 3D meshes (in `.obj`, `.mtl`, and `.png` formats) will be saved in a specified folder. This folder will be crucial for the next steps, so make sure to note its path carefully or copy them into another folder you create and note the new path.

### Step 3: Installing and Using BlenderProc

1. **Install BlenderProc**:
   ```bash
   pip install blenderproc
   ```

2. **Change Directory to BlenderProc Scripts**:
   ```bash
   cd BlenderProc/blenderproc/scripts
   ```

3. **Run `select_poly_all.py`**:
   - Update `mesh_dir` to point to the folder with your 3D models and set `destination_folder` to your desired output folder (e.g., `your_home_path/BlenderProc/blenderproc/scripts/output`).
   ```bash
   python select_poly_all.py
   ```

### Step 4: Additional Dependencies and Pre-Inpaint Processing

**Note**: Before proceeding, **cd out** of the BlenderProc directory.

1. **Install Required Packages**:
   ```bash
   pip install opencv-python numpy matplotlib
   ```

2. **Run `rename_file.py`**:
   - Ensure `folder_path` points to the directory containing the 3D meshes and mask files generated in Step 3.
   ```bash
   python rename_file.py
   ```

3. **Run `run.py`**:
   - Make sure that `input_path` and `output_path` match the `folder_path` set in `rename_file.py`.
   ```bash
   python run.py
   ```

4. **Create Folders in ZITS**:
   - If the `images`, `masks`, and `output` folders do not exist inside the ZITS directory, create them before running the next script.

### Step 5: Setting Up ZITS Inpainting Environment

1. **Prepare ZITS Folders**:
   - Set the following variables in `copy_to_zits.py`:
     - `source_dir`: Directory where your 3D meshes and masks are located.
     - `dest_dir_black`: Path to the `masks` folder inside `ZITS_inpainting` (`./ZITS_inpainting/masks`).
     - `dest_dir_apple`: Path to the `images` folder inside `ZITS_inpainting` (`./ZITS_inpainting/images`).

2. **Run `copy_to_zits.py`**:
   ```bash
   python copy_to_zits.py
   ```

3. **Set Up ZITS Inpainting**:
   - Open a new terminal.
   - Navigate to `ZITS_inpainting`:
     ```bash
     cd ZITS_inpainting
     ```
   - Create and activate a new Conda environment:
     ```bash
     conda create -n train_env python=3.6
     conda activate train_env
     ```
   - Install the required packages:
     ```bash
     pip install torch==1.9.0+cu111 torchvision==0.10.0+cu111 torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html
     pip install -r requirement.txt
     cd apex
     pip install -v --disable-pip-version-check --no-cache-dir --global-option="--cpp_ext" --no-build-isolation ./
     ```

4. **Run the Inpainting Script**:
   ```bash
   python single_image_test_script.py
   ```
   The inpainted textures will be saved in the `output` folder inside the `ZITS_inpainting` directory.

5. **Troubleshooting**:
   - If you encounter installation issues with ZITS, refer to their [GitHub page](https://github.com/DQiaole/ZITS_inpainting) for assistance.

### Step 6: Final Processing with Replace Script

1. **Run `replace.py`**:
   - Set the following paths:
     - `input_dir_original`: Directory where your 3D meshes and mask files are located.
     - `input_dir_mask`: The same directory as `input_dir_original`.
     - `input_dir_inpainted`: Path to the `output` folder from ZITS_inpainting.
     - `output_dir`: Set this to `/your_home_directory/BlenderProc/blenderproc/scripts/output`.
   ```bash
   python replace.py
   ```

### Steps 7 & 8: Final UV and JSON Updates

1. **Run `update_json.py`**:
   - Set the paths:
     - `input_folder = '/your_home_directory/BlenderProc/blenderproc/scripts/output'`
     - `output_folder = '/your_home_directory/BlenderProc/blenderproc/scripts/output_json_updated'`
   ```bash
   python update_json.py
   ```

2. **Run `update_uv_all.py`**:
   - Set the following paths in `update_uv_all.py`:
     - `mesh_dir = '/your_home_directory/blenderProc/BlenderProc/blenderproc/scripts/output'`
     - `destination_folder = '/your_home_directory/BlenderProc/BlenderProc/blenderproc/scripts/output_json_updated'`
     - `json_directory = '/your_home_directory/blenderProc/BlenderProc/blenderproc/scripts/output_json_updated'`
   ```bash
   python update_uv_all.py
   ```


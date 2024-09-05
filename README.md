# Generation of 3D Meshes Dataset

## Description

This project is dedicated to the generation and utilization of 3D meshes, particularly of fruits and vegetables. The project is divided into two main stages:

1. **Generation of 3D Meshes**: This stage involves creating detailed 3D meshes of various fruits and vegetables.
2. **Simulation and Dataset Creation**: Using the generated meshes, scenes are simulated using BlenderProc to create datasets, including the NOCS CAMERA dataset.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Ubuntu**: The project is developed and tested on Ubuntu.
- **Stable Diffusion 3**: Required for the generation of a high-quality dataset of images.
- **Instant Meshes**: Used for converting images to 3D meshes.
- **Blender**: Necessary for refining the 3D meshes.
- **BlenderProc**: Used for simulating scenes and creating the final datasets.

## Pipeline Overview

The project pipeline is divided into two main stages:
1. **Image Generation**: Generate a large dataset of images using Stable Diffusion.
2. **3D Mesh Generation and Simulation**: Convert the images into 3D meshes and simulate scenes using BlenderProc.

## Detailed Steps

### Step 1: Generating a Dataset of Images using Stable Diffusion 3

In this step, you will generate a dataset of images that will be used in subsequent stages to create 3D meshes.

1. **Create a Virtual Environment**:
   - First, create a virtual environment to manage your dependencies:
     ```bash
     python -m venv myenv
     ```
   - Activate the virtual environment:
     - On **Linux/Mac**:
       ```bash
       source myenv/bin/activate
       ```
     - On **Windows**:
       ```cmd
       . myenv/Scripts/activate
       ```

2. **Install Required Packages**:
   - Install the necessary Python packages:
     ```bash
     pip install diffusers torch transformers ipywidgets accelerate protobuf sentencepiece
     ```

3. **Prepare Directories**:
   - Create a folder where your images will be saved. This folder will be specified in the `image_generation.py` script.

4. **Update Path in Script**:
   - Make sure to update the path in the `image_generation.py` script to point to the folder you created for saving images.

5. **Run Image Generation Script**:
   - Execute the `image_generation.py` script to generate images:
     ```bash
     python image_generation.py
     ```
   - In this project, 10,000 images were generated for 50 categories of fruits using the `stabilityai/stable-diffusion-3-medium-diffusers` model.

### Step 2: Generating 3D Meshes with Instant Meshes

1. **Install Instant Meshes**:
   - Follow the detailed installation guide provided in the [Instant Mesh GitHub repository](https://github.com/TencentARC/InstantMesh) to ensure that Instant Meshes is properly installed.

2. **Run Instant Meshes**:
   - Once Instant Meshes is installed, convert the images to 3D meshes by running the following command:
     ```bash
     python run.py configs/instant-mesh-large.yaml path_to_your_saved_images --save_video --export_texmap
     ```
   - Replace `path_to_your_saved_images` with the path to the folder where your images are saved. This command will generate the 3D meshes, save a video of the process, and export the texture maps.

3. **Output**:
   - By the end of this step, you should have 10,000 3D models, each consisting of `.obj`, `.mtl`, and `.png` files.

### Step 3: Installing and Using BlenderProc

1. **Install BlenderProc**:
   - Install BlenderProc using pip:
     ```bash
     pip install blenderproc
     ```

2. **Navigate to the BlenderProc Scripts Directory**:
   - Change to the `BlenderProc/blenderproc/scripts` directory:
     ```bash
     cd BlenderProc/blenderproc/scripts
     ```

3. **Run `select_poly_all.py` Script**:
   - Prepare the script by updating the paths in `select_poly_all.py`:
     - Set `mesh_dir` to the folder where your 3D models are located (e.g., `3dmodels`).
     - Set `destination_folder` to your desired output directory (e.g., `your_home_path/BlenderProc/blenderproc/scripts/output`).
   - Execute the `select_poly_all.py` script:
     ```bash
     python select_poly_all.py
     ```

### Step 4: Installing Additional Dependencies and Final Execution

1. **Install Required Packages**:
   - Install the necessary Python packages for the pre-inpaint part:
     ```bash
     pip install opencv-python numpy matplotlib
     ```

2. **Prepare for `rename_file.py` Execution**:
   - Ensure that the `folder_path` in `rename_file.py` is set to the directory where your 3D meshes and the masks file generated in Step 3 are located.

3. **Run `rename_file.py` Script**:
   - Execute the `rename_file.py` script to rename files as needed:
     ```bash
     python rename_file.py
     ```

4. **Ensure Consistent Paths for `run.py`**:
   - Before running `run.py`, verify that `input_path` and `output_path` in the script are set to the same directory as `folder_path` used in `rename_file.py`.

5. **Run `run.py` Script**:
   - Execute the `run.py` script:
     ```bash
     python run.py
     ```

6. **Create Necessary Directories**:
   - Before running `copy_to_zits.py`, ensure that the following folders exist in the ZITS directory. If they do not exist, create them:
     - `images`
     - `masks`
     - `output`

7. **Run `copy_to_zits.py` Script**:
   - Finally, execute the `copy_to_zits.py` script:
     ```bash
     python copy_to_zits.py
     ```

### Step 5: Setting Up ZITS Inpainting Environment

1. **Open a New Terminal**:
   - Start by opening a new terminal window.

2. **Navigate to ZITS Directory**:
   - Change to the `ZITS_inpainting` directory:
     ```bash
     cd ZITS_inpainting
     ```

3. **Create and Activate Conda Environment**:
   - Create a new Conda environment with Python 3.6:
     ```bash
     conda create -n train_env python=3.6
     ```
   - Activate the Conda environment:
     ```bash
     conda activate train_env
     ```

4. **Install Dependencies**:
   - Install PyTorch and related libraries:
     ```bash
     pip install torch==1.9.0+cu111 torchvision==0.10.0+cu111 torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html
     ```
   - Install additional dependencies from the `requirements.txt` file:
     ```bash
     pip install -r requirement.txt
     ```

5. **Install Apex**:
   - Change to the `apex` directory and install Apex:
     ```bash
     cd apex
     pip install -v --disable-pip-version-check --no-cache-dir --global-option="--cpp_ext" --no-build-isolation ./
     ```

6. **Run Inpainting Script**:
   - After setting up the environment, run the `single_image_test_script.py` script:
     ```bash
     python single_image_test_script.py
     ```

### Step 6: Final Processing with Replace Script

1. **Run `replace.py` Script**:
   - Set the following paths in `replace.py`:
     - `input_dir_original`: Set this to the directory where your 3D meshes and the masks file (which are in the same folder) are located.
     - `input_dir_mask`: Set this to the same directory as `input_dir_original`.
     - `input_dir_inpainted`: Set this to the output folder from ZITS_inpainting.
     - `output_dir`: Set this to `/your_home_directory/BlenderProc/blenderproc/scripts/output`.
   - Execute the `replace.py` script:
     ```bash
     python replace.py
     ```

### Step 7: Final UV and JSON Updates

1. **Run `update_json.py` Script**:
   - Make sure the following paths are correctly set in `update_json.py`:
     - `input_folder = '/your_home_directory/BlenderProc/blenderproc/scripts/output'`
     - `output_folder = '/your_home_directory/BlenderProc/blenderproc/scripts/output_json_updated'`
   - Execute the `update_json.py` script to update your JSON file with neighbor search results:
     ```bash
     python update_json.py
     ```

2. **Run `update_uv_all.py` Script**:
   - Before running the script, ensure the following paths are updated in `update_uv_all.py`:
     - `mesh_dir = '/your_home_directory/BlenderProc/BlenderProc/blenderproc/scripts/output'`
     - `destination_folder = '/your_home_directory/BlenderProc/BlenderProc/blenderproc/scripts/output_json_updated'`
     - `json

_directory = '/your_home_directory/BlenderProc/BlenderProc/blenderproc/scripts/output_json_updated'`
   - Execute the `update_uv_all.py` script:
     ```bash
     python update_uv_all.py
     ```

This completes the pipeline!


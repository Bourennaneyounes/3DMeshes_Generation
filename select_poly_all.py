import blenderproc as bproc
import numpy as np
import bpy
import bmesh
import json
import shutil
import os
from PIL import Image, ImageDraw
import fnmatch

# Initialize BlenderProc
bproc.init()

# Path to the directory containing your mesh files
mesh_dir= "D:\\LIRIS Stage\\blender\\B\\BlenderProc\\A"
# Destination folder for the exported files
destination_folder = "D:\\LIRIS Stage\\blender\\B\\BlenderProc\\BlenderProc\\blenderproc\\scripts\\output"

# Ensure the destination folder exists
os.makedirs(destination_folder, exist_ok=True)

# Iterate through the directory to find all .obj files
for file_name in os.listdir(mesh_dir):
    if file_name.endswith(".obj"):
        # Construct file paths for the .obj, .mtl, and .png files
            # Path to your mesh files
            obj_file = os.path.join(mesh_dir, file_name)
            base_name = os.path.splitext(file_name)[0]
            mtl_file = os.path.join(mesh_dir, base_name + ".mtl")
            png_file = os.path.join(mesh_dir, base_name + ".png")

            # Extract filename without extension for use in saving the OBJ file
            base_name = os.path.splitext(os.path.basename(obj_file))[0]

            # Load the mesh object
            objs = bproc.loader.load_obj(obj_file)

            # Apply the material to the object
            for obj in objs:
                if obj.get_name().endswith(".mtl"):
                    obj.set_cp("use_nodes", True)
                    mat = obj.get_materials()[0]
                    mat.new_texture("Diffuse", png_file)

            # Create a point light next to the object
            light = bproc.types.Light()
            light.set_location([0, 4, 0])
            light.set_energy(300)

            # Set the camera to be in front of the object
            cam_pose = bproc.math.build_transformation_mat([0, 5, 0], [-np.pi / 2, -np.pi, 0])
            bproc.camera.add_camera_pose(cam_pose)

            # Render the scene
            data = bproc.renderer.render()

            # Switch to bpy to access edit mode and polygons
            for obj in objs:
                bpy_object = bpy.data.objects[obj.get_name()]  # Link BlenderProc object to bpy object
                bpy.context.view_layer.objects.active = bpy_object

                # Ensure object is in 'OBJECT' mode to access mesh data
                bpy.ops.object.mode_set(mode='OBJECT')

                # Get mesh data
                mesh = bpy_object.data
                camera = bpy.data.objects['Camera']

                # Ensure there is an active UV layer
                if not mesh.uv_layers:
                    print(f"Object {bpy_object.name} has no UV layers.")
                    continue

                uv_layer = mesh.uv_layers.active.data

                # Switch to 'EDIT' mode to use bmesh
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.reveal()  # Ensure all faces are selectable
                bpy.ops.mesh.select_all(action='DESELECT')

                # Create a BMesh object to work with
                bm = bmesh.from_edit_mesh(mesh)
                bm.faces.ensure_lookup_table()

                # Create a dictionary to hold selected polygons UV coordinates
                selected_polys_uv = {}
                selected_poly = []

                # Create a blank mask image (not used in the final script)
                width, height = 1024, 1024  # Size of the output mask image
                mask_image = Image.new('L', (width, height), 0)  # 'L' mode is for grayscale images
                draw = ImageDraw.Draw(mask_image)

                # Iterate over BMesh faces
                for face in bm.faces:
                    # Compute face center in world coordinates
                    face_center_world = bpy_object.matrix_world @ face.calc_center_median()
                    # Transform world coordinates to camera coordinates
                    face_center_camera = camera.matrix_world.inverted() @ face_center_world

                    # Check if face is in front of the camera
                    if face_center_camera.z > -4.3:
                        # Select the face
                        face.select = True
                        selected_poly.append(face.index)

                bmesh.update_edit_mesh(mesh)

                # Switch back to 'OBJECT' mode to access the final data
                bpy.ops.object.mode_set(mode='OBJECT')

                mesh = bpy_object.data
                if not mesh.uv_layers.active:
                    print("No UV layers found.")
                uv_layer = mesh.uv_layers.active.data

                for poly in mesh.polygons:
                    if poly.index in selected_poly:
                        # Collect UV coordinates for the selected polygon
                        poly_uvs = []
                        for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
                            uv = uv_layer[loop_index].uv
                            poly_uvs.append((int(uv.x * (width - 1)), int((1 - uv.y) * (height - 1))))  # Note: Flip Y-axis

                        # Debug print UV coordinates
                        print(f"Polygon {poly.index} UVs: {poly_uvs}")

                        # Draw the polygon on the mask (not used in the final script)
                        if poly_uvs:  # Ensure there are UV coordinates to draw
                            draw.polygon(poly_uvs, outline=255, fill=255)
                        selected_polys_uv[poly.index] = poly_uvs

                # Save the updated UV coordinates of selected polygons to a file
                # Save the updated UV coordinates of selected polygons to a file
                with open(os.path.join(destination_folder, f"{base_name}_selected_polys_uv.json"), "w") as f:
                    json.dump({int(k): v for k, v in selected_polys_uv.items()}, f, indent=4)

                mask_image.save(os.path.join(mesh_dir, f"{base_name}_mask.png"))

            # Export only the modified object to OBJ format
            bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects
            for obj in objs:
                bpy.data.objects[obj.get_name()].select_set(True)  # Select only the mesh objects

            output_obj_file = os.path.join(destination_folder, f"{base_name}.obj")
            bpy.ops.export_scene.obj(filepath=output_obj_file, use_selection=True, use_materials=True)

            # The MTL file is automatically saved alongside the OBJ file
            output_mtl_file = output_obj_file.replace(".obj", ".mtl")

            # Copy the original PNG file to the destination folder
            output_png_file = os.path.join(destination_folder, os.path.basename(png_file))
            shutil.copy(png_file, output_png_file)

            # Modify the MTL file to refer to the PNG in the destination folder
            with open(output_mtl_file, 'r') as file:
                mtl_data = file.readlines()

            # Replace the path of the texture
            for i, line in enumerate(mtl_data):
                if line.startswith('map_Kd'):
                    mtl_data[i] = f"map_Kd {base_name}.png\n"
                    break

            # Write the changes back to the MTL file
            with open(output_mtl_file, 'w') as file:
                file.writelines(mtl_data)

            print(f"Exported OBJ file: {output_obj_file}")
            print(f"Exported MTL file: {output_mtl_file}")
            print(f"Copied PNG file to: {output_png_file}")


print("Done with the process !!!!!!!!!!!!!.")
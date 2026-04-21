import os
import shutil

# Replace these with your actual folder paths
# Use the 'r' before the string to prevent errors with backslashes on Windows
source_root = r"C:\Users\UTKARSH\Desktop\sanatiry_waste\Dataset\Raw"
destination_folder = r"C:\Users\UTKARSH\Desktop\waste_classification_model\data\raw\sanitary_waste"
images_per_folder = 167

# The specific subfolders you listed
target_folders = [
    "blood_soaked_bandages", 
    "iv_bottles", 
    "used_masks", 
    "used_medical_gloves", 
    "used_medical_paper", 
    "used_syringes"
]

os.makedirs(destination_folder, exist_ok=True)

for subfolder in target_folders:
    subfolder_path = os.path.join(source_root, subfolder)
    
    if os.path.exists(subfolder_path):
        print(f"Processing: {subfolder}...")
        
        # Get only files (ignore any accidental sub-directories)
        images = [f for f in os.listdir(subfolder_path) if os.path.isfile(os.path.join(subfolder_path, f))]
        
        # Take exactly 167 images
        for i, img_name in enumerate(images[:images_per_folder]):
            old_path = os.path.join(subfolder_path, img_name)
            
            # Create the new name: e.g., "used_syringes_image1.jpg"
            new_name = f"{subfolder}_{img_name}"
            new_path = os.path.join(destination_folder, new_name)
            
            shutil.copy2(old_path, new_path)
    else:
        print(f"Warning: Could not find folder {subfolder}. Skipping.")

print("Copying complete!")
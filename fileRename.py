import os

folder_path = 'testImages'

# Get the list of files in the folder
file_names = os.listdir(folder_path)

# Separate the files into JPG and text files
jpg_files = [file for file in file_names if file.lower().endswith(('.jpg', '.jpeg'))]

# Sort the file lists alphabetically
jpg_files.sort()

# Rename the files
for i, (jpg_file) in enumerate(jpg_files, 1):
    # Rename JPG file
    jpg_file_new = f'testPlate{i}.jpg'
    jpg_file_path = os.path.join(folder_path, jpg_file)
    jpg_file_new_path = os.path.join(folder_path, jpg_file_new)
    os.rename(jpg_file_path, jpg_file_new_path)
    print(f'Renamed "{jpg_file}" to "{jpg_file_new}"')
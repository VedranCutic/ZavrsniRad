import os


def rename_files_in_folder(folder_path):
    # Get a list of all files in the folder
    files = os.listdir(folder_path)
    # Filter out directories, only keep files
    files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]

    # Loop over all files and rename them
    for index, filename in enumerate(files, start=1):
        # Define the new name
        new_name = f"slika_{index}{os.path.splitext(filename)[1]}"
        # Define the full paths
        old_file = os.path.join(folder_path, filename)
        new_file = os.path.join(folder_path, new_name)
        # Rename the file
        os.rename(old_file, new_file)
        print(f"Renamed '{filename}' to '{new_name}'")


# Specify the folder path
folder_path = "primjeri"

# Call the function
rename_files_in_folder(folder_path)

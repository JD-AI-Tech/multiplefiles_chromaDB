import os
import shutil

def write_files_to_folder(file_list, folder_name):
    try:
        # Create the folder if it doesn't exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Move each file to the folder
        for file_path in file_list:
            # Get the file name from the file path
            file_name = os.path.basename(file_path)
            print(f"write files to folder() file_name = {file_name}")
            # Construct the destination path by joining the folder path and file name
            destination_path = os.path.join(folder_name, file_name)
            print(f"destination_path = {destination_path}")
            # Move the file to the destination folder
           # shutil.move(file_path, destination_path)

        print("Files successfully saved!")
    except Exception as e:
        print("An error occurred:", str(e))

#  usage
if __name__ == "__main__":
    files = ["file1.txt", "file2.txt", "file3.txt"]
    folder = "data"

    write_files_to_folder(files, folder)

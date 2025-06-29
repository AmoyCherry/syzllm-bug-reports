import os
import shutil

filtered_description = ["WARNING", "INFO: ", "possible deadlock"]

def remove_warning_subfolders(root_folder):
    for subdir, dirs, files in os.walk(root_folder):
        # Only look at immediate subfolders
        for d in dirs:
            desc_path = os.path.join(subdir, d, "description")
            if os.path.isfile(desc_path):
                with open(desc_path, "r") as f:
                    content = f.read()
                if any(s in content for s in filtered_description):
                    shutil.rmtree(os.path.join(subdir, d))
        # Prevent descending into subfolders we might delete
        break

if __name__ == "__main__":
    root_folder = "./workdir/crashes"  # Change this to your folder path
    remove_warning_subfolders(root_folder)
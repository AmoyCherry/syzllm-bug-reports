import os
import shutil

filtered_description = ["WARNING", "INFO: ", "possible deadlock", "unregister_netdevice"]

def remove_warning_subfolders(root_folder):
    for subdir, dirs, files in os.walk(root_folder):
        for d in dirs[:]:  # Create a copy of dirs to avoid modifying while iterating
            subfolder_path = os.path.join(subdir, d)
            # Check if subfolder still exists (in case it was deleted)
            if not os.path.exists(subfolder_path):
                continue

            # Check description file
            desc_path = os.path.join(subfolder_path, "description")
            repro_path = os.path.join(subfolder_path, "repro.cprog")

            # Delete if description contains filtered strings or repro.cprog is missing
            should_delete = False
            if os.path.isfile(desc_path):
                with open(desc_path, "r") as f:
                    content = f.read()
                if any(s in content for s in filtered_description):
                    should_delete = True
            if not os.path.isfile(repro_path):
                should_delete = True

            if should_delete:
                shutil.rmtree(subfolder_path)

        # Prevent descending into subfolders
        break

if __name__ == "__main__":
    root_folder = "./workdir/crashes"
    remove_warning_subfolders(root_folder)
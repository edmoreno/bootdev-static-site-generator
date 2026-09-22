import os
import shutil


def copy_files_recursive(source_dir: str, destination_dir: str) -> None:
    if not os.path.exists(source_dir):
        raise Exception(f"{source_dir} does not exist!")

    # delete existing destination dir and recreate it
    if os.path.exists(destination_dir):
        print(os.path.exists(destination_dir))
        shutil.rmtree(destination_dir)
    os.mkdir(destination_dir)

    # copy files over from source to destination recursively
    for file in os.listdir(source_dir):
        full_source_path = os.path.join(source_dir, file)
        full_destination_path = os.path.join(destination_dir, file)
        if os.path.isfile(full_source_path):
            shutil.copy(full_source_path, full_destination_path)
        else:
            copy_files_recursive(full_source_path, full_destination_path)

    return None
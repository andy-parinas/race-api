import os



def get_root_dir():
    # Get the absolute path of the current script
    script_path = os.path.abspath(__file__)
    
    # Get the directory containing the script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    # Get the root directory by traversing up one or more levels
    root_directory = os.path.abspath(os.path.join(script_directory, '..'))

    return root_directory


def get_storage_dir():
    root_dir = get_root_dir()
    return f"{root_dir}/storage"
from pathlib import Path
from utils.db_loader import load_db

if __name__ == "__main__":
    print("Main Executing")
    path_root = Path(__file__).parents[1]

    file = f"{str(path_root)}/storage/20221119_GOS_FORM_XML_A.xml"
    load_db(file)

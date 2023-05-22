import os
from pathlib import Path
from utils.db_loader import load_db
from utils.sftp_client import get_files_in_dir, create_ssh_client



if __name__ == "__main__":
    print("Main Executing")


    files = get_files_in_dir('/mr_form')

    print(files)

    # path_root = Path(__file__).parents[1]


    # files = [
    #     "20221119_GOS_FORM_XML_A.xml",
    #     # "20221119_BAR_FORM_XML_A.xml",
    #     # "20221119_GCO_FORM_XML_A.xml",
    #     # "20221119_KEG_FORM_XML_A.xml",
    #     # "20221119_MPK_FORM_XML_A.xml",
    #     # "20221119_SUN_FORM_XML_A.xml"
    # ]

    # for file in files:
    #     xml_file = f"{str(path_root)}/storage/{file}"
    #     load_db(xml_file)

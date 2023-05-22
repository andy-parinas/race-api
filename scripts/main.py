from pathlib import Path
from utils.db_loader import load_db

if __name__ == "__main__":
    print("Main Executing")
    path_root = Path(__file__).parents[1]


    files = [
        "20221119_GOS_FORM_XML_A.xml",
        # "20221119_BAR_FORM_XML_A.xml",
        # "20221119_GCO_FORM_XML_A.xml",
        # "20221119_KEG_FORM_XML_A.xml",
        # "20221119_MPK_FORM_XML_A.xml",
        # "20221119_SUN_FORM_XML_A.xml"
    ]

    for file in files:
        xml_file = f"{str(path_root)}/storage/{file}"
        load_db(xml_file)

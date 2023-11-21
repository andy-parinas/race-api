import sys
import os
from pathlib import Path
from datetime import datetime
from utils.sftp_client import sftp_client
from app import repositories as repo
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from utils.xml_parser import XmlParser
from utils.scratch_loader import load_scratch
from app.schemas.scratch_files import ScratchFileCreate, ScratchFile
from utils.s3_client import S3Client
from app.settings import settings



path_root = Path(__file__).parents[1]

def is_valid_date(date_string):
    try:
        # Parse the date string using the specified format
        datetime.strptime(date_string, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def get_start_params(db: Session, arguments: str):

    args = arguments[0]

    if args == 'today':
        now = datetime.now()
        unix_time = int(now.timestamp())
        return unix_time

    elif is_valid_date(args):
        return datetime.strptime(args, "%d/%m/%Y").timestamp()

    else:
        latest_file = repo.scratch_files.get_latest_scratch_file(db)
        if latest_file is not None:
            return latest_file.timestamp

    return None


def delete_file_from_local_storage(file_path: str):
    if os.path.exists(file_path):
        print(f"File exists in local storage, deleting file...")
        try:
            os.remove(file_path)
            print("File deleted successfully.")
        except OSError as e:
            print(f"Error occurred while deleting the file: {e}")


def upload_scratched_file(downloaded_file, filename: str):
    try:
        s3_client = S3Client(settings.S3_REGION, settings.FORM_BUCKET)
        s3_client.upload_file(
            downloaded_file, settings.SCRATCH_FOLDER, filename)
        print("Scratch File Uploaded: ", filename)

    except Exception as e:
        print(f"error uploading file: {filename}\n")
        print(e)


def process_file(db: Session, filename: str, timestamp: int):
    file_path = f"{str(path_root)}/storage/{filename}"

    if os.path.exists(file_path):
        delete_file_from_local_storage(file_path)

    downloaded_file = sftp_client.download_file(
        '/mr_scratchings', filename, f"{str(path_root)}/storage")

    if downloaded_file:
        print(f"File downloaded successfully: {downloaded_file}")

        load_scratch(downloaded_file)

        upload_scratched_file(downloaded_file, filename)

        scratch_in_db = repo.scratch_files.get_by_filename(db, filename)
        if scratch_in_db is None:
            print("Saving Scratch filename to db \n")
            scratch_file = repo.scratch_files.create(db,ScratchFileCreate(
                file_name=filename, is_processed=True, is_uploaded=False, timestamp=timestamp
            ))

        else:
            print("Scratch File Exist in DB. No action taken \n")
        delete_file_from_local_storage(downloaded_file)


if __name__ == "__main__":
    print("Scratch Executing")

    files = sftp_client.get_files_in_dir('/mr_scratchings')

    arguments = sys.argv
    arguments = arguments[1:]

    db = SessionLocal()
    start_timestamp = get_start_params(db, arguments)

    if start_timestamp is not None:
        for file in files:
            filename = file.filename
            if file.st_mtime > start_timestamp:
                process_file(db, filename, timestamp=start_timestamp)


    #
    # xml_file = file
    # parser = XmlParser(xml_file)
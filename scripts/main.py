from typing import List
import os
import sys
import glob
from pathlib import Path
from datetime import datetime
from sqlalchemy.orm import Session
from utils.db_loader import load_db
from utils.sftp_client import sftp_client
from utils.s3_client import S3Client
from app import repositories as repo
from app.db.session import SessionLocal
from app.schemas.form_files import FormFilesCreate, FormFiles
from app.settings import settings
from utils.image_download import image_download


path_root = Path(__file__).parents[1]


def load_file_to_db(db: Session, downloaded_file, file: FormFiles):
    try:
        load_db(downloaded_file)
        repo.form_files.set_processed(db, file.id)
        print("File Processed: ", file.file_name)

    except Exception as e:
        print(f"error processing file: {file.file_name}\n")
        print(e)


def upload_processed_file(db: Session, downloaded_file, file: FormFiles):
    try:
        s3_client = S3Client(settings.S3_REGION, settings.FORM_BUCKET)
        s3_client.upload_file(
            downloaded_file, settings.FORM_FOLDER, file.file_name)
        repo.form_files.set_uploaded(db, file.id)
        print("File Uploaded: ", file.file_name)
        delete_file_from_local_storage(downloaded_file)

    except Exception as e:
        print(f"error uploading file: {file.file_name}\n")
        print(e)


def delete_file_from_local_storage(file_path: str):
    if os.path.exists(file_path):
        print(f"File exists in local storage, deleting file...")
        try:
            os.remove(file_path)
            print("File deleted successfully.")
        except OSError as e:
            print(f"Error occurred while deleting the file: {e}")


def process_file(db: Session, filename: str, timestamp: int):

    # check if file exists in local storage
    file_path = f"{str(path_root)}/storage/{filename}"

    if os.path.exists(file_path):
        delete_file_from_local_storage(file_path)

    downloaded_file = sftp_client.download_file(
        '/mr_form', filename, f"{str(path_root)}/storage")

    if downloaded_file:
        print(f"File downloaded successfully: {downloaded_file}")

        file_in_db = repo.form_files.get_form_file_from_filename(
            db, filename=filename)

        if not file_in_db:
            print("File not in DB. Creating FormFile entry...")
            file_in_db = repo.form_files.create(db, FormFilesCreate(
                file_name=filename, is_processed=False, is_uploaded=False, timestamp=timestamp
            ))

        # process the File
        print(f"Loading {filename} contents into DB... ")
        load_file_to_db(db, downloaded_file, file_in_db)

        # Update Timestamp
        repo.form_files.update_timestamp(
            db, file_in_db.id, timestamp=timestamp)

        # upload the file to S3
        if not file_in_db.is_uploaded:
            upload_processed_file(db, downloaded_file, file_in_db)

        delete_file_from_local_storage(downloaded_file)


def update_file(db: Session, file: str, timestamp: int):
    # check if file exists in local storage
    file_path = f"{str(path_root)}/storage/{file}"

    if os.path.exists(file_path):
        delete_file_from_local_storage(file_path)

    downloaded_file = sftp_client.download_file(
        '/mr_form', file, f"{str(path_root)}/storage")

    try:
        load_db(downloaded_file, update=True)
        repo.form_files.set_processed(db, file.id)
        print("File Processed: ", file.file_name)

    except Exception as e:
        print(f"error processing file: {file.file_name}\n")


def is_valid_date(date_string):
    try:
        # Parse the date string using the specified format
        datetime.strptime(date_string, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def get_start_params(db: Session, arguments: List[str]):
    params = {}

    for arg in arguments:
        parts = arg.split('=')
        if len(parts) == 2:
            param, value = parts
            params[param] = value

    latest_file = repo.form_files.get_latest_form_file(db)

    if 'start' in params:
        if params['start'] == 'today':
            now = datetime.now()
            unix_time = int(now.timestamp())
            return unix_time
        elif is_valid_date(params['start']):
            pass
        else:
            if latest_file:
                return latest_file.timestamp
    else:
        if latest_file:
            return latest_file.timestamp


if __name__ == "__main__":
    print("Main Executing")

    arguments = sys.argv
    arguments = arguments[1:]

    # db = SessionLocal()
    # for file in file_list:
    #     print(f"Processing file: {file} ")
    #     filename = file.split("/")[-1]
    #     if filename.endswith("_A.xml"):
    #         load_db(file)

### WORKING #####

    files = sftp_client.get_files_in_dir('/mr_form')
    # print(files)

    db = SessionLocal()
    start_timestamp = get_start_params(db, arguments)

    for file in files:
        filename = file.filename
        if filename.endswith("_A.xml"):
            if file.st_mtime > start_timestamp:

                process_file(
                    db, filename, timestamp=file.st_mtime)
                # if not file_db_exists:
                #     process_file(
                #         db, filename, timestamp=file.st_mtime)
                # else:
                #     print(
                #         f"File in DB already exists: {file_db_exists.file_name}")
                #     process_file(
                #         db, filename, timestamp=file.st_mtime, file_in_db=file_db_exists)

                #     if file.st_mtime > file_db_exists.timestamp:
                #         print("Perform update on file...")

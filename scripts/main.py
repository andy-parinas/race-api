import os
import re
from pathlib import Path
from sqlalchemy.orm import Session
from utils.db_loader import load_db
from utils.sftp_client import sftp_client
from utils.s3_client import s3_client
from app import repositories as repo
from app.db.session import SessionLocal
from app.schemas.form_files import FormFilesCreate, FormFiles


def load_file_to_db(db: Session, downloaded_file, file: FormFiles):
    try:
        load_db(downloaded_file)
        repo.form_files.set_processed(db, file.id)
        print("File Processed: ", file.file_name)

    except Exception as e:
        print(f"error processing file: {file.file_name}\n")


def upload_processed_file(db: Session, downloaded_file, file: FormFiles):
    try:
        s3_client.upload_file(downloaded_file, 'form', file.file_name)
        repo.form_files.set_uploaded(db, file.id)
        print("File Uploaded: ", file.file_name)
        delete_file_from_local_storage(downloaded_file)

    except Exception as e:
        print(f"error uploading file: {file.file_name}\n")


def delete_file_from_local_storage(file_path: str):
    if os.path.exists(file_path):
        print(f"File exists in local storage, deleting file...")
        try:
            os.remove(file_path)
            print("File deleted successfully.")
        except OSError as e:
            print(f"Error occurred while deleting the file: {e}")


def process_file(db: Session, file: str, timestamp: int, is_new: bool = False):

    # check if file exists in local storage
    file_path = f"{str(path_root)}/storage/{file}"

    if os.path.exists(file_path):
        delete_file_from_local_storage(file_path)

    downloaded_file = sftp_client.download_file(
        '/mr_form', file, f"{str(path_root)}/storage")

    if downloaded_file:
        print(f"File downloaded successfully: {downloaded_file}")
        if is_new:
            file_in_db = repo.form_files.create(db, FormFilesCreate(
                file_name=file, is_processed=False, is_uploaded=False, timestamp=timestamp
            ))
        else:
            file_in_db = repo.form_files.get_form_file_from_filename(db, file)

        # process the File
        if not file_in_db.is_processed:
            load_file_to_db(db, downloaded_file, file_in_db)

        # upload the file to S3
        if not file_in_db.is_uploaded:
            upload_processed_file(db, downloaded_file, file_in_db)


if __name__ == "__main__":
    print("Main Executing")
    path_root = Path(__file__).parents[1]

    files = sftp_client.get_files_in_dir('/mr_form')
    # # print(files)

    # for file in files:
    #     # parse_file(file)
    #     print(file.filename)
    #     print(file.st_mtime)

    db = SessionLocal()
    for file in files:
        print(f"Processing file: {file} ")
        filename = file.filename
        file_db_exists = repo.form_files.get_form_file_from_filename(
            db, filename=filename)
        if not file_db_exists:
            process_file(db, filename, is_new=True)
        else:
            print(f"File in DB already exists: {file_db_exists.filename}")
            if file.st_mtime > file_db_exists.timestamp:
                print("Perform update on file...")
            elif file.st_mtime == file_db_exists.timestamp:
                process_file(
                    db, filename, timestamp=file.st_mtime, is_new=False)

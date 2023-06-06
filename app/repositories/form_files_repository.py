from typing import List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, update

from app.models.form_files import FormFiles
from app.schemas.form_files import FormFilesCreate, FormFiles as FormFilesSchema


class FormFilesRepository:

    def create(self, db: Session, obj_in: FormFilesCreate):
        horse_obj = obj_in.dict()
        db_obj = FormFiles(**horse_obj)
        db.add(db_obj)
        db.commit()
        return FormFilesSchema.from_orm(db_obj)

    def get_form_file_from_filename(self, db: Session, filename: str) -> FormFilesSchema:
        form_file = db.query(FormFiles).filter(
            FormFiles.file_name == filename).first()
        if not form_file:
            return None

        return FormFilesSchema.from_orm(form_file)

    def get_latest_form_file(self, db: Session):
        stmt = select(FormFiles).order_by(FormFiles.timestamp.desc())

        form_file = db.scalars(stmt).first()

        if not form_file:
            return None

        return FormFilesSchema.from_orm(form_file)

    def set_processed(self, db: Session, id: int):
        try:
            db.query(FormFiles).filter(FormFiles.id == id).update(
                {FormFiles.is_processed: True})
            db.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def set_uploaded(self, db: Session, id: int):
        try:
            db.query(FormFiles).filter(FormFiles.id == id).update(
                {FormFiles.is_uploaded: True})
            db.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def update_timestamp(self, db: Session, id: int, timestamp: int):
        stmt = update(FormFiles).where(FormFiles.id == id).returning(FormFiles).values(
            timestamp=timestamp
        )

        form_file = db.scalars(stmt).first()

        return FormFilesSchema.from_orm(form_file)


form_files = FormFilesRepository()

from sqlalchemy.orm import Session, joinedload
from app.models.sratch_files import ScratchFiles
from app.schemas.scratch_files import ScratchFile as ScratchFileSchema, ScratchFileCreate
from sqlalchemy import select, update
from typing import Optional

class ScratchFilesRepository:

    def get_latest_scratch_file(self, db: Session):
        stmt = select(ScratchFiles).order_by(ScratchFiles.timestamp.desc())

        scratch_file = db.scalars(stmt).first()

        if not scratch_file:
            return None

        return ScratchFileSchema.from_orm(scratch_file)

    def get_by_filename(self, db: Session, filename: str) -> Optional[ScratchFileSchema]:
        form_file = db.query(ScratchFiles).filter(
            ScratchFiles.file_name == filename).first()
        if not form_file:
            return None

        return ScratchFileSchema.from_orm(form_file)

    def create(self, db: Session, obj_in: ScratchFileCreate)->ScratchFileSchema:
        horse_obj = obj_in.dict()
        db_obj = ScratchFiles(**horse_obj)
        db.add(db_obj)
        db.commit()
        return ScratchFileSchema.from_orm(db_obj)


scratch_files = ScratchFilesRepository()
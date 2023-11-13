from sqlalchemy.orm import Session, joinedload
from app.models.sratch_files import ScratchFiles
from app.schemas.scratch_files import ScratchFile as ScratchFileSchema
from sqlalchemy import select, update

class ScratchFilesRepository:

    def get_latest_scratch_file(self, db: Session):
        stmt = select(ScratchFiles).order_by(ScratchFiles.timestamp.desc())

        scratch_file = db.scalars(stmt).first()

        if not scratch_file:
            return None

        return ScratchFileSchema.from_orm(scratch_file)


scratch_files = ScratchFilesRepository()
from pydantic import BaseModel

class ScratchFileBase(BaseModel):
    file_name: str
    is_processed: bool
    is_uploaded: bool
    timestamp: int


class ScratchFileInDb(ScratchFileBase):
    id: int

    class Config:
        orm_mode = True


class ScratchFile(ScratchFileInDb):
    ...


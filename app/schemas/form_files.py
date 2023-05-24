from pydantic import BaseModel


class FormFilesBase(BaseModel):
    file_name: str
    is_processed: bool
    is_uploaded: bool
    timestamp: int


class FormFilesCreate(FormFilesBase):
    ...


class FormFilesInDb(FormFilesBase):
    id: int

    class Config:
        orm_mode = True


class FormFiles(FormFilesInDb):
    ...

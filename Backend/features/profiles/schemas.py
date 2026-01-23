from pydantic import BaseModel

class ProfileBase(BaseModel):
    name: str

class ProfileCreate(ProfileBase):
    pass

class ProfileResponse(ProfileBase):
    id: int

    class Config:
        from_attributes = True

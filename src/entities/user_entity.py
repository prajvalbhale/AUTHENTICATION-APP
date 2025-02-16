from pydantic import BaseModel

class UserEntity(BaseModel):
    userName: str
    userMail: str
    phone: str
    address: str
    role: str
    created_by: int

    class Config:
        from_attributes = True

from pydantic import BaseModel

class CreateUserDTO(BaseModel):
    userName: str
    password: str
    userMail: str
    phone: str
    address: str
    role: str

class TokenDTO(BaseModel):
    access_token: str
    token_type: str

class UpdateUserDTO(BaseModel):
    userName: str
    userMail: str
    phone: str
    address: str
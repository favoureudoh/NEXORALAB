from pydantic import BaseModel, EmailStr


# This is what we expect when someone registers
class MemberRegister(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr  # validates it is actually an email format
    username: str
    password: str


# This is what we expect when someone logs in
class MemberLogin(BaseModel):
    email: EmailStr
    password: str


# This is what we send back to the frontend about a member
# Notice: no password field — we never send passwords back
class MemberOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    username: str

    class Config:
        from_attributes = True

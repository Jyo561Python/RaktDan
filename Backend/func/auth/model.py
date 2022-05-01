from pydantic import BaseModel, Field, EmailStr

class UserSchema(BaseModel):
    userid: str = Field(default=None)
    fullname: str = Field(default=None)
    email: EmailStr = Field(default=None)
    gender: str = Field(default=None)
    dob: str = Field(default=None)
    blood_group: str = Field(default="unknown")
    aadhar: int = Field(default=None)
    class Config:
        the_schema = {
            "user": {
                "userid": {"type": "string", "required": True},
                "fullname": {"type": "string", "required": True},
                "email": {"type": "string", "required": True},
                "gender": {"type": "string", "required": True},
                "dob": {"type": "string", "required": True},
                "blood_group":{"type": "string", "required": True},
                "aadhar": {"type": "integer", "required": True}
            }
        }

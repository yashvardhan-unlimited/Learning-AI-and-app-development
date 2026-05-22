from pydantic import BaseModel,EmailStr, field_validator, model_validator,computed_field,Field
import re
from datetime import datetime
from typing import Literal

class Student(BaseModel):
    Roll: int = Field(...,
                      length=8,
                      example=25110357)
    Name: str = Field(example="Yashvardhan Gupta"),
    Addmision_year: int =Field(lenght=4,
                                example=2025)
    Branch: str = "None"
    
class signup(BaseModel):
    email: EmailStr
    password: str 
    confirm_password: str
    @field_validator('password','confirm_password')
    def username_length(cls, value):
        if not re.search(r"[A-Za-z]", value):
            raise ValueError("Password must contain an alphabet")

        if not re.search(r"\d", value):
            raise ValueError("Password must contain a number")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain a special character")

        return value
    
    @model_validator(mode='after')
    def password_match(cls, values):
        if values.password != values.confirm_password:
            raise ValueError('Password do not match')
        return values
    
    DOB: datetime

    number1: int
    number2: int
    operation: Literal["+","-","*","/","%","^"]
    
    
    

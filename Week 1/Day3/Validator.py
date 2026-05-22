from pydantic import BaseModel,EmailStr, field_validator, model_validator,computed_field,Field
import re
from datetime import datetime
from typing import Literal, List, Optional

class Address(BaseModel):
    street: str
    city: str
    postal_code: str

class Student(BaseModel):
    Roll: int = Field(...,
                      length=8,
                      example=25110357)
    Name: str = Field(example="Yashvardhan Gupta"),
    Addmision_year: int =Field(length=4,
                                example=2025)
    Branch: str = "None"
    Address: Address
    
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

class Calculator(BaseModel):
    number1: float
    number2: float
    operation: Literal["+","-","*","/","%","^"]

    @computed_field
    @property
    def Calc(self)->float: 
        if self.operation=="+": 
            return self.number1 + self.number2
        elif self.operation=="-":
            return self.number1 - self.number2
        elif self.operation=="*":
            return self.number1 * self.number2
        elif self.operation=="/":
            if self.number2 == 0:
                raise ValueError("Cannot divide by zero")
            return self.number1 / self.number2
        elif self.operation=="%":
            if self.number2 == 0:
                raise ValueError("Cannot modulo by zero")
            return self.number1 % self.number2
        elif self.operation=="^":
            return self.number1 ** self.number2
    
class Comment(BaseModel):
    id: int
    content: str
    replies: Optional[List['Comment']] = None

Comment.model_rebuild()




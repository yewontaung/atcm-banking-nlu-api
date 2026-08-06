from pydantic import EmailStr, Field

from app.dtos.base import BaseDto


class PredictionForm(BaseDto):
    text:str

class APIKeyForm(BaseDto):
    user_id:int
    project_name:str

class AccountForm(BaseDto):
    full_name:str
    email:EmailStr
    password:str = Field(min_length=6)
    confirm_password:str = Field(min_length=6)

    @property
    def valid(self) -> bool:
        return self.password == self.confirm_password
from pydantic import BaseModel, field_validator
from pydantic_core import PydanticCustomError
from validate_email_address import validate_email

from .books import ReturnedSellerBook

__all__ = ["IncomingSeller", "ReturnedSeller", "ReturnedAllSellers", "ReturnedSellerWithBooks", "LoginSeller"]


class BaseSeller(BaseModel):
    first_name: str
    last_name: str
    email: str


class IncomingSeller(BaseSeller):
    password: str

    @field_validator("email")
    @staticmethod
    def validate_email(val: int):
        if not validate_email(val):
            raise PydanticCustomError("Validation error", "Email is wrong!")
        return val


class ReturnedSeller(BaseSeller):
    id: int


class ReturnedSellerWithBooks(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    books: list[ReturnedSellerBook]


class ReturnedAllSellers(BaseModel):
    sellers: list[ReturnedSeller]


class LoginSeller(BaseModel):
    email: str
    password: str

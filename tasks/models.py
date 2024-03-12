from pydantic import BaseModel


class Person(BaseModel):
    time: str
    name: str
    email: str
    phone: str
    accommodation: str



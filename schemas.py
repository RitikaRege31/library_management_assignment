from typing import TypedDict

class BookSchema(TypedDict):
    title: str
    author: str
    published_year: int

class MemberSchema(TypedDict):
    name: str
    email: str

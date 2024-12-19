# from typing import TypedDict

# class BookSchema(TypedDict):
#     title: str
#     author: str
#     published_year: int

# class MemberSchema(TypedDict):
#     name: str
#     email: str
from typing import TypedDict, Optional

class BookSchema(TypedDict):
    title: str
    author: str
    published_year: int
    member_id: Optional[int]  # This is the ID of the member to whom the book is issued. It can be None if not issued.

class MemberSchema(TypedDict):
    name: str
    email: str

class BookResponseSchema(TypedDict):
    id: int
    title: str
    author: str
    published_year: int
    status: str  # The status field will indicate whether the book is issued or not.

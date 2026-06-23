from pydantic import BaseModel

class BaseUser (BaseModel):
    username: str
    email: str
    bio: str = ""

class SearchUser(BaseModel):
    username: str | None = None
    email: str | None = None
    bio: str | None = None

class PatchUser (BaseModel):
    username: str | None = None
    email: str | None = None
    bio: str | None = None

from models.general import BaseDB

class BaseUser (BaseDB):
    username: str
    email: str
    bio: str = ""

class PatchUser (BaseDB):
    username: str | None = None
    email: str | None = None
    bio: str | None = None

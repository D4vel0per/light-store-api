from datetime import datetime, timezone

from beanie import Insert, Replace, SaveChanges, Update, before_event
from pydantic import BaseModel, Field

class BaseDB(BaseModel):
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = None

    @before_event(Insert)
    def set_created_at(self):
        self.created_at = datetime.now(timezone.utc)

    @before_event(Update, SaveChanges, Replace)
    def set_updated_at(self):
        self.updated_at = datetime.now(timezone.utc)
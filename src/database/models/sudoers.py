from datetime import datetime
from typing import Optional

from beanie import Document
from pydantic import Field


class Sudoers(Document):

    class Settings:
        name = 'sudoers'
        keep_nulls = False
        use_cache = True
        use_revision = True
        use_state_management = True
        state_management_replace_objects = True

    user_id: int
    added_by: int
    updated_by: Optional[int] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

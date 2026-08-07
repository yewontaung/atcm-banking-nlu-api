from typing import Optional

from app.dtos.base import BaseDto


class APIKeySearch(BaseDto):
    q:Optional[str] = None
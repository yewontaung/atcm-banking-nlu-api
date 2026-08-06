from typing import Any, Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

class BaseDto(BaseModel):

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )

class ModificationResult(BaseDto):
    result_item:Any
    success:bool
    message:Optional[str] = None
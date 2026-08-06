from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, ForeignKeyConstraint, Relationship, SQLModel

from app.data.enums import APIKeyStatus, AccountRole


class Account(SQLModel):

    account_id:Optional[int] = Field(primary_key=True, default=None)
    full_name:str = Field(nullable=False)
    account_email:str = Field(unique=True, nullable=False)
    hashed_password:str = Field(nullable=False)
    account_role:AccountRole = Field(nullable=False, default=AccountRole.Member)

    api_keys:list["APIKey"] = Relationship(back_populates="creator")

class APIKey(SQLModel):
    key_id:Optional[int] = Field(primary_key=True, default=None)
    api_key:str = Field(unique=True, nullable=False)
    status:APIKeyStatus = Field(nullable=False, default=APIKeyStatus.ACTIVE)

    created_at:datetime = Field(default_factory=lambda:datetime.now(tz=timezone.utc))
    updated_at:datetime = Field(default_factory=lambda:datetime.now(tz=timezone.utc))
    created_by:int = Field(nullable=False)
    updated_by:int = Field(nullable=False)
    creator:Optional[Account] = Relationship(back_populates="api_keys")

    __table_args__ = (
        ForeignKeyConstraint(
            ["created_by"],
            ["account.account_id"],
            name="fk_api_key_creator",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["updated_by"],
            ["account.account_id"],
            name="fk_api_key_updator",
        ),
    )
from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, ForeignKeyConstraint, Relationship, SQLModel

from app.data.enums import APIKeyStatus, AccountRole


class Account(SQLModel, table=True):

    account_id:Optional[int] = Field(primary_key=True, default=None)
    full_name:str = Field(nullable=False)
    account_email:str = Field(unique=True, nullable=False)
    hashed_password:str = Field(nullable=False)
    account_role:AccountRole = Field(nullable=False, default=AccountRole.MEMBER)
    created_at:datetime = Field(default_factory=lambda:datetime.now(tz=timezone.utc))
    updated_at:datetime = Field(default_factory=lambda:datetime.now(tz=timezone.utc))

    api_keys:list["APIKey"] = Relationship(back_populates="creator", sa_relationship_kwargs={
        "foreign_keys": "[APIKey.created_by]"
    })

class APIKey(SQLModel, table=True):
    key_id:Optional[int] = Field(primary_key=True, default=None)
    project_name:str = Field(nullable=False)
    hashed_api_token:str = Field(unique=True, nullable=False, index=True)
    status:APIKeyStatus = Field(nullable=False, default=APIKeyStatus.ACTIVE)

    created_at:datetime = Field(default_factory=lambda:datetime.now(tz=timezone.utc))
    updated_at:datetime = Field(default_factory=lambda:datetime.now(tz=timezone.utc))
    created_by:int = Field(nullable=False)
    updated_by:Optional[int] = Field(default=None)
    creator:Optional[Account] = Relationship(back_populates="api_keys", sa_relationship_kwargs={
        "foreign_keys": "[APIKey.created_by]"
    })
    updator:Optional[Account] = Relationship(sa_relationship_kwargs={
        "foreign_keys": "[APIKey.updated_by]"
    })

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
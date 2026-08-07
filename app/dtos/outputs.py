from datetime import datetime
from typing import Optional

from pydantic import computed_field

from app.data.enums import APIKeyStatus, AccountRole
from app.data.models import APIKey, Account
from app.dtos.base import BaseDto


class AuthResult(BaseDto):

    account_id:int

    access_token:str
    access_type:str = "Bearer"

    @computed_field
    @property
    def token_string(self) -> str:
        return f"{self.access_type} {self.access_token}"

class AccountProfile(BaseDto):
    account_id:int
    full_name:str
    account_email:str
    account_role:AccountRole
    created_at:datetime
    updated_at:datetime | None

    @staticmethod
    def from_(account:Account) -> "AccountProfile":
        return AccountProfile(
            account_id=account.account_id,
            full_name=account.full_name,
            account_email=account.account_email,
            account_role=account.account_role,
            created_at=account.created_at,
            updated_at=account.updated_at,
        )

class APIKeyResult(BaseDto):
    key_id:int
    project_name:str
    api_key:str
    message:str
    creator_id:int
    creator_name:str
    created_at:datetime
    status:APIKeyStatus

class APIKeyListItem(BaseDto):
    key_id:int
    project_name:str
    creator_id:int
    creator_name:str
    creator_email:str
    status:APIKeyStatus
    created_at:datetime
    updated_at:datetime
    updator_id:Optional[int] = None
    updator_name:Optional[str] = None
    updator_email:Optional[str] = None
    updator_role:Optional[AccountRole] = None

    def from_(api_key:APIKey) -> "APIKeyListItem":
        creator = api_key.creator
        updator = api_key.updator
        return APIKeyListItem(
            key_id=api_key.key_id,
            project_name=api_key.project_name,
            status=api_key.status,
            creator_id=creator.account_id,
            creator_email=creator.account_email,
            creator_name=creator.full_name,
            created_at=api_key.created_at,
            updator_id=updator.account_id if updator else None,
            updator_name=updator.full_name if updator else None,
            updator_email=updator.account_email if updator else None,
            updated_at=api_key.updated_at,
            updator_role=updator.account_role if updator else None,
        )

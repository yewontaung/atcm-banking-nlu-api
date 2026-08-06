from enum import Enum


class AccountRole(str, Enum):
    ADMIN = "Admin"
    MEMBER = "Member"

class APIKeyStatus(str, Enum):
    ACTIVE = "Active"
    DEACTIVATED = "Deactivated"
    DELETED = "Deleted"
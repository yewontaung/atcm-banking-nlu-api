from sqlmodel import Session, func, select

from app.data.enums import APIKeyStatus
from app.data.models import APIKey, Account
from app.dtos.outputs import DashboardInfo


def get_stats(session:Session) -> DashboardInfo:
    total_users = session.exec(
        select(func.count(Account.account_id))
    ).one_or_none() or 0

    total_keys = session.exec(
        select(func.count(APIKey.key_id))
    ).one_or_none() or 0

    active_keys = session.exec(
        select(func.count(APIKey.key_id)).where(APIKey.status == APIKeyStatus.ACTIVE)
    ).one_or_none() or 0

    deactived_keys = session.exec(
        select(func.count(APIKey.key_id)).where(APIKey.status == APIKeyStatus.DEACTIVATED)
    ).one_or_none() or 0

    return DashboardInfo(
        total_users=total_users,
        total_keys=total_keys,
        active_keys=active_keys,
        deactivated_keys=deactived_keys,
    )
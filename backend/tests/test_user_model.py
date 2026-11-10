import pytest
from sqlalchemy.exc import IntegrityError

from app.models import User, UserRole


async def test_user_defaults(session):
    session.add(User(telegram_id=111))
    await session.commit()
    user = (await session.get(User, 1))
    assert user.role is UserRole.USER
    assert user.is_blocked is False
    assert user.notifications_enabled is True
    assert user.created_at is not None


async def test_telegram_id_unique(session):
    session.add(User(telegram_id=222))
    await session.commit()
    session.add(User(telegram_id=222))
    with pytest.raises(IntegrityError):
        await session.commit()

import logging

import pytest

from app.core.config import Settings
from app.core.logging import RedactingFilter


def test_cors_origins_comma_separated():
    s = Settings(cors_origins="http://a.com, http://b.com")
    assert s.cors_origins == ["http://a.com", "http://b.com"]


def test_production_requires_real_secret():
    with pytest.raises(ValueError):
        Settings(app_env="production")


def test_production_rejects_wildcard_cors():
    with pytest.raises(ValueError):
        Settings(app_env="production", jwt_secret="x" * 32, cors_origins=["*"])


def test_production_ok():
    s = Settings(app_env="production", jwt_secret="x" * 32)
    assert s.app_env == "production"


def test_log_filter_redacts_secrets():
    f = RedactingFilter()
    token = "123456789:" + "A" * 35
    record = logging.LogRecord("t", logging.INFO, "", 0, f"bot {token} init_data=abc123&x=1", None, None)
    f.filter(record)
    assert token not in record.msg and "abc123" not in record.msg

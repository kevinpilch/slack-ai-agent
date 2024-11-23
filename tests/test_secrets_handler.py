import logging
import pytest

from pytest import MonkeyPatch, LogCaptureFixture

from src.utils.secrets_handler import get_secrets


def test_get_secrets_local_env(monkeypatch: MonkeyPatch, caplog: LogCaptureFixture) -> None:

    monkeypatch.setenv("APP_ENV", "local")
    monkeypatch.setenv("SLACK_BOT_TOKEN", "test_token")
    monkeypatch.setenv("SLACK_SIGNING_SECRET", "test_secret")
    caplog.set_level(logging.INFO)

    token, secret = get_secrets()

    assert "App environment: local. Loading secrets from environment." in caplog.text
    assert token == "test_token"
    assert secret == "test_secret"


def test_get_secrets_non_local_env(monkeypatch: MonkeyPatch, caplog: LogCaptureFixture) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    caplog.set_level(logging.INFO)

    with pytest.raises(Exception, match="Non-local secret management not yet implemented."):
        get_secrets()

    assert "App environment: deployed. Loading secrets from secrets manager." in caplog.text
import os
from unittest.mock import patch

from src.slack_ai_agent.slack import load_bot_user_id

def test_load_bot_user_id_should_load_slack_user_id_env_var() -> None:
    with patch("src.slack_ai_agent.slack.WebClient") as MockWebClient:
        mock_instance = MockWebClient.return_value
        mock_instance.auth_test.return_value = {"user_id": "test_user_id"}

        load_bot_user_id()
        slack_user_id_env_var = os.environ.get("SLACK_USER_ID")

        assert slack_user_id_env_var == "test_user_id"

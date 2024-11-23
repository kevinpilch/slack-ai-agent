import os
from logging import getLogger

from dotenv import load_dotenv

logger = getLogger(__name__)


def get_secrets() -> tuple[str, str]:
    env = os.environ.get("APP_ENV")
    if env == "local":
        logger.info("App environment: local. Loading secrets from environment.")
        load_dotenv()
        slack_bot_token = os.environ.get("SLACK_BOT_TOKEN", "NO SLACK_BOT_TOKEN SET")
        slack_signing_secret = os.environ.get("SLACK_SIGNING_SECRET", "NO SLACK_SIGNING_SECRET SET")
        return slack_bot_token, slack_signing_secret
    else:
        logger.info("App environment: deployed. Loading secrets from secrets manager.")
        raise Exception("Non-local secret management not yet implemented.")

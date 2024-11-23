import os
import logging
from typing import Any

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt.context.say import Say
from slack_bolt import App
from flask import Flask, request
from flask.wrappers import Response

from src.utils.secrets_handler import get_secrets

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

slack_bot_token, slack_signing_secret = get_secrets()
slack_app = App(
    token=slack_bot_token,
    signing_secret=slack_signing_secret
)
handler = SlackRequestHandler(slack_app)

flask_app = Flask(__name__)

def load_bot_user_id() -> None:
    """
    Gets the bot user ID via the Slack API and loads it to the SLACK_USER_ID environment variable.
    """
    try:
        slack_client = WebClient(token=slack_bot_token)
        response = slack_client.auth_test()
        os.environ["SLACK_USER_ID"] = response["user_id"]
    except SlackApiError as e:
        logger.error(f"Could not load bot user ID: {e}")
        raise e


def shout(text: str) -> str:
    return text.upper()


@slack_app.event("app_mention")
def handle_mentions(body: dict[str, Any], say: Say) -> None:
    """
    Event listener for mentions in Slack.
    When the Slack AI bot is mentioned, this function processes the message text and sends response.

    Args:
        body (dict): The event data received from Slack.
        say (callable): A function for sending a response to the channel.
    """
    text = body["event"]["text"]

    slack_bot_user_id = os.environ.get("SLACK_USER_ID")
    mention = f"<@{slack_bot_user_id}>"
    text = text.replace(mention, "").strip()

    say("Working on it, give me a sec...")
    response = shout(text)
    say(response)


@flask_app.route("/health", methods=["GET"])
def health_check() -> tuple[str, int]:
    return "OK", 200


@flask_app.route("/slack/events", methods=["POST"])
def slack_events() -> Response:
    """
    Route for handling Slack events.
    This function passes the incoming HTTP request to the SlackRequestHandler for processing.

    Returns:
        Response: The result of handling the request.
    """
    logger.info("Headers: %s", dict(request.headers))
    logger.info("Body: %s", request.get_data())
    return handler.handle(request)


if __name__ == "__main__":
    load_bot_user_id()
    flask_app.run()

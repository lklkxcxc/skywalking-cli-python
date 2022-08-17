#!/usr/bin/env python3
import logging
import os
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# WebClient instantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token='xoxb-3836226053254-3945220451778-VtVFfKjM0eNmB1yJw1R0L08w')
logger = logging.getLogger(__name__)
# ID of channel you want to post message to
channel_id = "C03QSR196NN"
def send_message(msg,png):
  try:
    response = client.files_upload(
       channels=channel_id,
       file=png,
       filetype="png",
       title="upload percentile.png"
    )
    pic_url=response['file']['url_private']
  except SlackApiError as e:
    print(f'Error {e}')

  try:
    # Call the conversations.list method using the WebClient
    result = client.chat_postMessage(
        channel=channel_id,
        blocks=[
            {
                "type": "section",
                "text":{
                    "type": "mrkdwn",
                    "text": msg
                },
                "accessory": {
                "type": "image",
                "image_url": pic_url,
                "alt_text": "Percentile image"
                 }
            }
        ]
        # You could also use a blocks[] array to send richer content
    )
    # Print result, which includes information about the message (like TS)
    print(result)

  except SlackApiError as e:
    print(f'Error {e}')
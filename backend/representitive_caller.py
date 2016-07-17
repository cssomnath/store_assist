__author__ = 'kuolin'
from slacker import Slacker
slack = Slacker('xoxp-56179022755-59194962325-60464736370-d7b0f5db09')
def call_sells():
    # Send a message to #general channel
    slack.chat.post_message('#sells', 'Sells representative please come to gate 1.')

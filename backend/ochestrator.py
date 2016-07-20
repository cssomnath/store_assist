__author__ = 'kuolin'
import os
import json
import decimal
import sys
import time
import configparser
import boto3
from botocore.exceptions import ClientError
from slacker import Slacker
config = configparser.ConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), "app.config"))
import photo_capture
from monitorer import Monitor
from faceplusplusclient import FacePPClient
dynamodb = boto3.resource('dynamodb', region_name=config.get('Dynamo','region-name'), endpoint_url=config.get('Dynamo','endpoint-url'))
table = dynamodb.Table(config.get('Dynamo','table-name'))
monitor_item_id=int(config.get('Dynamo','monitor-item-id'))
subscription_key=config.get('MicrosoftFace','subscription-key')
slack_key=config.get('Slack','api-key')
slack_channel=config.get('Slack','channel')
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

class Ochestrater:
    def __init__(self):
        self.initialize_check_id()
        self.face_client=FacePPClient(subscription_key)
        self.monitor=Monitor()
        self.slacker=Slacker('api-key')
    def initialize_check_id(self):
        try:
            response = table.get_item(
                Key={
                    'Id': monitor_item_id
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'],file=sys.stderr)
            raise Exception('Initialization Error')
        else:
            item = response['Item']
            self.id=item['Num_Id']
            self.sells=item['Num_Rep']
            print('Initialize Id: '+str(self.id))
            print('Initialize Rep Num: '+str(self.sells))

    def check_trigger(self):
        try:
            response = table.get_item(
                Key={
                    'Id': monitor_item_id
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'],file=sys.stderr)
            return False
        else:
            item = response['Item']
            id=item['Num_Id']
            sells=item['Num_Rep']
            if sells>self.sells:
                self.sells=sells
                print('New sells: '+str(self.sells))
                self.slacker.chat.post_message(slack_channel, 'Sells representative please come to gate 1.')
            if id>self.id:
                self.id=id
                print('New Id: '+str(self.id))
                return True
            return False

    def start_monitoring(self):
        while(1):
            time.sleep(3)
            if self.check_trigger():
                filename=photo_capture.capture(str(self.id)+'.jpg')
                self.face_client.process(filename)
            #     self.monitor.triggered=True
            # else:
            #     self.monitor.monite()

def main():
    ochestrater=Ochestrater()
    ochestrater.start_monitoring()
if __name__ == '__main__':
    main()

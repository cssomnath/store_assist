__author__ = 'kuolin'
import boto3
from botocore.exceptions import ClientError
import json
import decimal
import sys
import time
import photo_capture
from monitorer import Monitor
from faceplusplusclient import FacePPClient
from representitive_caller import *
dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")
table = dynamodb.Table('ProductCatalog')

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
        self.face_client=FacePPClient()
        self.monitor=Monitor()
    def initialize_check_id(self):
        try:
            response = table.get_item(
                Key={
                    'Id': 123
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
                    'Id': 123
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
                call_sells()
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
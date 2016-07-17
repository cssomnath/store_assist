__author__ = 'kuolin'
import numpy as np
import cv2
import sys
import photo_capture
import time
import boto3
from botocore.exceptions import ClientError
dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")
table = dynamodb.Table('ProductCatalog')

class Monitor:
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    find_last_time=False
    triggered=False
    def monite(self):
        photo_capture.capture('tmp.jpg')
        img = cv2.imread('tmp.jpg')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        x,y,_=img.shape
        img_thread_hold=x*y*0.07
        for face in faces:
            _,_,width,height=face
            print(face)
            if (width*height)>img_thread_hold:
                print('1')
                if self.find_last_time:
                    print('3')
                    if not self.triggered:
                        print('4')
                        print('Detect face, trigger downstream.')
                        self.increament_encounter()
                        self.triggered=True
                else:
                    print('2')
                    self.find_last_time=True
            else:
                print('5')
                self.triggered=False
        if len(faces)==0:
            print('6')
            self.find_last_time=False
            self.triggered=False
    def increament_encounter(self):
        try:
            response = table.get_item(
                Key={
                    'Id': 123
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'],file=sys.stderr)
        id=response['Item']['Num_Id']
        id+=1
        response = table.update_item(
            Key={
                'Id': 123
            },
            UpdateExpression="set Num_Id = :r",
            ExpressionAttributeValues={
                ':r': id
            },
            ReturnValues="UPDATED_NEW"
        )


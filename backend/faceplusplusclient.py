__author__ = 'kuolin'
import json
import requests
import os,sys
class FacePPClient:
    api_key='f991a286bb66459553a0fcf40a27b89a'
    api_secret='ZtaL6eozjOqBBFg5ounC3MZF1G4oGlSX'
    headers = {'Content-Type':'application/octet-stream','Ocp-Apim-Subscription-Key':'58ceffd8e4f14b47bc7d218e8513c3d3'}
    def get_information(self,img_path):
        with open(img_path,'rb') as infile:
            img_data=infile.read()
            response = requests.post(url="https://api.projectoxford.ai/face/v1.0/detect?returnFaceId=true&returnFaceLandmarks=false&returnFaceAttributes=age,gender,smile",
                                     headers=self.headers,
                                     data=img_data,
                                     timeout=120)
            return json.loads(response.content.decode('UTF-8'))

    def process_informations(self,face_informations):
        age=[]
        gender=[]
        smile=[]
        for face in face_informations:
            age.append(face['faceAttributes'].get('age',None))
            gender.append(face['faceAttributes'].get('gender',None))
            smile.append(face['faceAttributes'].get('smile',None))
            return age,gender,smile

    def process(self,img_path):
        face_informations=self.get_information(img_path)
        if face_informations:
            ages,genders,smiles= self.process_informations(face_informations)
            with open('output.txt','a') as outfile:
                for face in zip(ages,genders,smiles):
                    print(img_path,face[0],face[1],face[2],sep='\t',end='\n',file=outfile)
            with open('output_newest.txt','w') as outfile:
                for face in zip(ages,genders,smiles):
                    print(img_path,face[0],face[1],face[2],sep='\t',end='\n',file=outfile)
def main():
    image=sys.argv[1]
    client=FacePPClient()
    face_informations=client.get_information(image)
    #face_informations=json.loads('[{"faceId":"425c5f3d-8d10-490e-bcbd-29f003df4fff","faceRectangle":{"top":184,"left":322,"width":182,"height":182},"faceAttributes":{"smile":1.0,"gender":"male","age":30.1}}]')
    ages,genders,smiles= client.process_informations(face_informations)
    for face in zip(ages,genders,smiles):
        print(image,face[0],face[1],face[2],sep='\t')

def batch():
    image_folder='images/'
    client=FacePPClient()
    for image_name in os.listdir(image_folder):
        face_informations=client.get_information(image_folder+image_name)
        ages,genders,smiles= client.process_informations(face_informations)
        for face in zip(ages,genders,smiles):
            print(image_name,face[0],face[1],face[2],sep='\t')

if __name__ == '__main__':
    main()
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from PIL import Image
import json
def index(request):
    return render(request, 'index.html')

def image(request):
    try:
        with open("/Users/kuolin/Documents/PycharmProjects/untitled3/newest.jpg", "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    except:
        red = Image.new('RGBA', (1, 1), "white")
        response = HttpResponse(content_type="image/jpeg")
        red.save(response, "JPEG")
        return response

def information(request):
    try:
        with open("/Users/kuolin/Documents/PycharmProjects/untitled3/output_newest.txt", "r") as f:
            information=f.readline().strip().split('\t')
            data={'id':information[0].replace('.jpg',''),'age':information[1],'gender':information[2],'smile':information[3]}
            return HttpResponse(json.dumps(data), content_type="application/json")
    except:
        response = HttpResponse(json.dumps({'id':None,'age':None,'gender':None,'smile':None}),content_type="application/json")
        return response

def past_information(request):
    try:
        with open("/Users/kuolin/Documents/PycharmProjects/untitled3/output_history.txt", "r") as f:
            ages=[]
            gender=[]
            smile=[]
            id=[]
            for line in f:
                print(line)
                information=line.strip().split('\t')
                id.append(information[0].replace('.jpg',''))
                ages.append(information[1])
                gender.append(information[2])
                smile.append(information[3])
            data={'id':id,'age':ages,'gender':gender,'smile':smile}
            return HttpResponse(json.dumps(data), content_type="application/json")
    except:
        response = HttpResponse(json.dumps({'id':None,'age':None,'gender':None,'smile':None}),content_type="application/json")
        return response
from django.shortcuts import redirect, render, HttpResponse
#from creditcardfd.models import Contact
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import uploadForm
from .models import upload1
from .utils import dataview1, dist_plot, line_chart,pred,analysis,get_barchart,dist_plot,get_heatmap,line_chart
import pandas as pd
import json
import pickle
import os
import mimetypes
# Create your views here.
def index(request):
    return render(request, 'index.html')
def home(request,pk=0):
    return render(request, 'index.html')
def about(request):
    return render(request, 'about.html')
#     # return HttpResponse("this is aboutpage")
def signin(request):
      if request.method == "POST":
          user=request.POST["username"]
          pass1=request.POST["pass1"]
          user = authenticate(username=user, password=pass1)
        
          if user is not None:
              login(request, user)
              messages.success(request, "Logged In Sucessfully!!")
              return redirect('home1')
          else:
              messages.error(request, "Bad Credentials!!")
              return redirect('home')
    

      return render(request, 'signin.html')
#     # return HttpResponse("this is service page")
def home1(request,pk=0):
    if request.method == 'POST':
        form = uploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = uploadForm()
    return render(request, 'index1.html', {
        'form': form
    })
def dashboard(request,pk=0):
    uploads=upload1.objects.all()
    return render(request,'dasboard.html',{'uploads':uploads})


def deleteupload(request,pk):
    if request.method == "POST":
        upload =upload1.objects.get(pk=pk)
        upload.delete()
    return redirect('dashboard')


def dataview(request,pk):
    if request.method == "POST":
        upload =upload1.objects.get(pk=pk)
        name=upload.uploadfile
        data1=dataview1(name)
        context = {'d': data1,'upload':upload}
    return render(request, 'dataview.html', context)



def prediction(request,pk):
    if request.method == "POST":
        upload =upload1.objects.get(pk=pk)
        name=upload.uploadfile
        df=pred(name)
        filename="Complete_predictive_result.csv"
        t='media/download/'+filename
        df.to_csv(t)
        df=df.head(500)
        json_records = df.reset_index().to_json(orient ='records')
        data = []
        data = json.loads(json_records)
        context = {'d': data,'upload':upload, 'file':filename}
    return render(request,'prediction.html',context)

def Analysis(request,pk):
    if request.method == "POST":
        upload =upload1.objects.get(pk=pk)
        name=upload.uploadfile
        name1=name
        print(name)
        anarray=analysis(name)
        dis_plot=dist_plot()
        barchart=get_barchart(anarray["fraud"],anarray["nonfcount"])
        corr=get_heatmap(name1)
        
        line_chart1=line_chart()
        global context
        context = {'d': anarray,'upload':upload,'dis_plot':dis_plot ,'barchart':barchart,"corr":corr,"line_chart":line_chart1}
    return render(request,'Analysis.html',context)

def line(request,pk=0):
    if request.method == "POST":
        var=request.POST['cars']
        line=line_chart(var)
        context.update({"line_chart":line})
    return render(request,'Analysis.html',context)
def about1(request,pk=0):
    return render(request,'about1.html')
def download(request,filename):
   if filename != '':
        # Define Django project base directory
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Define the full file path
        filepath = 'media/download/' + filename
        # Open the file for reading content
        path = open(filepath, 'rb')
        # Set the mime type
        mime_type, _ = mimetypes.guess_type(filepath)
        # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type=mime_type)
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        # Return the response value
        return response
def advCproject(request):
    return render(request,'advCproject.html')
def easyJproject(request):
    return render(request,'easyJproject.html')
def intmJproject(request):
    return render(request,'intmJproject.html')
def advJproject(request):
    return render(request,'advJproject.html')
def contact(request):
   # if request.method == "POST":
       # name = request.POST['name']
       # email = request.POST['email']
       # phone = request.POST['phone']
        #desc = request.POST['desc']
        #C1 = Contact(name=name,email=email,phone=phone,desc=desc,date=datetime.today())
       # C1.save()
       # messages.success(request, 'Profile Successfuly Saved')
    return render(request,'contact.html')


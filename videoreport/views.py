from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import os
from .forms import ReportForm
from .backend import start_checking
#from django.utils.encoding import smart_str
import mimetypes

global csrf_temp_token
csrf_temp_token=["one"]

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def get_report(request):
    context={}
    path = 'media/'
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        
        # create a form instance and populate it with data from the request:
        form = ReportForm(request.POST)
        # check whether it's valid:
        print(form.is_valid())
        print(request.FILES, "request file")
        #temp=str(type(request.FILES['document'])).lower()
        context['form']=form
        print(len(request.POST))
        print(request.POST)
        if "document" in request.FILES and csrf_temp_token[-1]!=request.POST['csrfmiddlewaretoken']:
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            csrf_temp_token.remove(csrf_temp_token[-1])
            csrf_temp_token.append(request.POST['csrfmiddlewaretoken'])
            uploaded_file = request.FILES['document']
            if uploaded_file.name.endswith(".avi") or uploaded_file.name.endswith(".mp4") or uploaded_file.name.endswith(".webm") or uploaded_file.name.endswith(".m4v"):
                fs = FileSystemStorage()
                remove_files(path)
                name = fs.save(uploaded_file.name, uploaded_file)
                context['upload']='YES'
                context['url'] = fs.url(name)
                context['message']='File Uploaded Successfully'
                #request.FILES=None
                video_path=path+uploaded_file.name
                red_start_time=request.POST['start_time']
                red_duration=request.POST['red_duration']
                green_duration=request.POST['green_duration']
                yellow_duration=request.POST['yellow_duration']
                date_time=request.POST['video_taken_time']
                stop_line_type=request.POST['position']
                start_checking(video_path, red_start_time, red_duration, green_duration, yellow_duration, date_time, stop_line_type)
                return render(request, 'download.html')
            else:
                context['message']='Upload a valid Video'
            return render(request, 'home.html', context)
            #return redirect('')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ReportForm()

    return render(request, 'home.html', {'form': form})
    
def remove_files(path):
    files_in_dir = os.listdir(path)
    for f in files_in_dir:
        os.remove(f'{path}{str(f)}')
        
def download(request):
    path='/static_files/Violated_cars/violated_data.csv'
    return render(request, 'download.html', {'url': path})
    
def download_file(request):
    fl_path = '/static/Violated_cars/'
    filename = 'violated_data.csv'
    fl = open(fl_path, 'r')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response
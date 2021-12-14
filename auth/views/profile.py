from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models import Students, Teachers
from itertools import chain
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from ..utils import find_emotion
from datetime import datetime, time

@login_required(login_url="login")
def detect(request):
    if request.method == "POST":
        new_file = request.FILES['audio_data']
        file_name = request.user.first_name+".wav"
        file_name = file_name.replace(" ","")
        path = default_storage.save(file_name, ContentFile(new_file.read()))
        path = "media/"+path
        return redirect("response",find_emotion(path))
    return render(request, "auth/rec.html")

@login_required(login_url="login")
def response(request,emotion):
    now = datetime.now()
    now_time = now.time()
    response_path = emotion+".wav"
    data = render_to_string("data.html",{"data_body": "Listen Songs at","data_link": "https://www.spotify.com/us/",})
    if now_time >= time(21,00) or now_time <= time(8,00):
        response_path = "response/night_" + response_path
    else:
        response_path = "response/day_" + response_path
    return render(request,"auth/response.html", {"emotion": emotion,"resp":response_path,"data":data})
    



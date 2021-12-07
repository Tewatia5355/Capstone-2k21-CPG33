from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Students, Teachers
from itertools import chain
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from ..utils import find_emotion
from datetime import datetime

@login_required(login_url="login")
def detect(request):
    if request.method == "POST":
        new_file = request.FILES['audio_data']
        file_name = request.user.first_name+".wav"
        file_name = file_name.replace(" ","")
        path = default_storage.save(file_name, ContentFile(new_file.read()))
        path = "media/"+path
        print("\n\n",path,"\n\n")
        return JsonResponse({"Emotion Detected":find_emotion(path)})
    return render(request, "auth/rec.html")
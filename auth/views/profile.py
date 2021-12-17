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
    extension = ".wav"
    response_path = emotion
    data_body , data_link = "",""
    if now_time >= time(21,00) or now_time <= time(8,00):
        if emotion == "happy":
            data_body = "Listen Songs at"
            data_link = "https://www.spotify.com/us/"
        elif emotion == "sad":
            data_body = "Wanna listen to some sleep playlist at"
            data_link = "https://www.spotify.com/us/"
        elif emotion == "angry":
            extension = ".mp3"
            data_body = "Wanna listen to some calm playlist at"
            data_link = "https://www.spotify.com/us/"
        elif emotion == "surprise":
            data_body = "Share your excitement on Social Media"
            data_link = "https://www.facebook.com/"
        elif emotion == "disgust":
            extension = ".mp3"
            data_body = "Watch something on Youtube to divert your mind"
            data_link = "https://www.youtube.com/"
        elif emotion == "fear":
            data_body = "Wanna listen to some sleep playlist at"
            data_link = "https://www.spotify.com/us/"
        else:
            data_body = "Wanna listen to some sleep playlist at"
            data_link = "https://www.spotify.com/us/"
        response_path = "response/night_" + response_path + extension
    else:
        if emotion == "happy":
            data_body = "Glad to hear you're happy!"
            data_link = ""
        elif emotion == "sad":
            data_body = "You can connect to a close friend on social media"
            data_link = "https://www.facebook.com/"
        elif emotion == "angry":
            extension = ".mp3"
            data_body = "Count from 1-10 and listen to a calm playlist at"
            data_link = "https://www.spotify.com/us/"
        elif emotion == "surprise":
            data_body = "Tell me more about it."
            data_link = ""
        elif emotion == "disgust":
            data_body = "Watch something on Youtube to divert your mind"
            data_link = "https://www.youtube.com/"
        elif emotion == "fear":
            data_body = "Watch some Yoga videos and calm down"
            data_link = "https://www.youtube.com/"
        else:
            data_body = "Wanna order some food online"
            data_link = "https://www.zomato.com"
        response_path = "response/day_" + response_path + extension
    data = render_to_string("data.html",{"data_body": data_body,"data_link": data_link,})
    return render(request,"auth/response.html", {"emotion": emotion,"resp":response_path,"data":data})
    



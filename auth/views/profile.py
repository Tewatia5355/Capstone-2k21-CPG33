from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Students, Teachers
from itertools import chain
from django.http import JsonResponse


@login_required(login_url="login")
def detect(request):
    if request.method == "POST":
        data = (request.user.last_name).split(",")
        age = int(data[0])
        gender = data[1]
        return JsonResponse({"message": "Success"})

    return render(request, "auth/rec.html")


from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .serializers import *
from rest_framework import status
import json
# Create your views here.

@api_view(['GET'])
@csrf_exempt
def show_all_profiles(request):
    if request.method=='GET':
        profiles=Profile.objects.all()
        print(json.dumps(list(profiles.values('id','name'))))
        profile_serializer=ProfileSerializer(profiles,many=True)
        data=profile_serializer.data
        return JsonResponse(
            data=data,
            safe=False,
            status=status.HTTP_200_OK
        )

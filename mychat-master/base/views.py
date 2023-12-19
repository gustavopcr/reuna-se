from django.shortcuts import render
from django.http import JsonResponse
import random
import time
from agora_token_builder import RtcTokenBuilder
from .models import RoomMember
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required



# Create your views here.
user_locations = []
def login(request):
    if request.method == "POST":

        username = request.POST.get('uname', '')
        password = request.POST.get('psw', '')
    
        
        if username == "user" and password == "password":

            return redirect('lobby')
        else:
            return render(request, 'base/login.html', {'error': 'Invalid credentials'})
    

    return render(request, 'base/login.html')

def lobby(request):
    return render(request, 'base/lobby.html')

def room(request):
    return render(request, 'base/room.html')


def getToken(request):
    appId = "4364e66536334cce88db2580451626fd"
    appCertificate = "5988a393b17843eabdba9a7154580e99"
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    print('body')
    print(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    #print('createMember')
    #print(data["lat"])
    user_locations.append({'lat': data["lat"], 'lng': data["lng"]})

    return JsonResponse({'name':data['name']}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name':member.name}, safe=False)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    member.delete()
    return JsonResponse('Member deleted', safe=False)

@csrf_exempt
def get_user_locations(request):
    print('🚀 ~ file: views.py:96 ~ request:', request.body)
    # Fetch user locations from the database or any source
    print('teste')
    print(user_locations)
    #user_locations = [
    #    {'lat': 40.7128, 'lng': -74.0060},  # Example location 1 (New York)
    #    {'lat': 34.0522, 'lng': -118.2437},  # Example location 2 (Los Angeles)
    #    {'lat': 38.0522, 'lng': -90.2437},
        # Add more user locations here
    #]

    return JsonResponse({'locations': user_locations})
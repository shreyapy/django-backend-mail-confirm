from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings
from django.core.mail import send_mail
from .forms import StatusForm
from .models import Status
from .serializers import StatusSerializer
from .utils.helper import encrypt, decrypt
from django.core import serializers

from django.contrib.auth.models import User
from .serializers import UserSerializer

@api_view(['POST'])
@permission_classes((AllowAny,))
def login(req):
    username = req.data.get("username")
    password = req.data.get("password")
    if username is None or password is None:
        return Response({'msg': 'Please provide both username and password'})
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'msg': 'Invalid Credentials'})
    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        'username': user.username,
        'email': user.email,
        'name': user.first_name + ' ' + user.last_name,
        'token': token.key
    })

@api_view(['POST'])
@permission_classes((AllowAny,))
def signup(req):

    username = req.data.get("username")
    password = req.data.get("password")
    email = req.data.get("email")
    first_name = req.data.get("first_name")
    last_name = req.data.get("last_name")

    if(username is None or password is None or email is None or first_name is None
        or username == "" or password == "" or email == "" or first_name == ""):
        return Response({'msg' : 'Please provide all the credentials'})

    if(User.objects.filter(username=username)):
        return Response({'msg' : 'Username already taken'})

    user = User.objects.create_user(
        username,
        email = email,
        password = password,
        first_name = first_name,
        last_name = last_name,
        is_superuser = False,
        is_staff = False
    )
    
    status_form = StatusForm(req.POST)
    if(status_form.is_valid()):
        user.save()
        status = status_form.save(commit=False)
        status.user = user
        status.save()

    send_mail(
        'ToTick Account Confirmation',
        f'Hi {first_name} {last_name},\n\nYour account has been successfully with username: {username}'
        '\n\nClick on the link to verify your email : https://todo-rest-app-django.herokuapp.com/auth/verifyEmail/'+encrypt(username),
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently = False
    )

    return Response({'msg': 'Account created successfully'})

@api_view(['GET'])
@permission_classes((AllowAny,))
def verifyEmail(req, id):
    try:
        username = decrypt(id)
        user = User.objects.get(username = username)
        status = Status.objects.get(user = user)
        form = StatusForm({'isActive': True}, instance = status)
        if(form.is_valid()):
            status = form.save(commit=False)
            status.user = user
            status.save()
        return Response({'msg':'Email Verified'})
    except Exception as e:
        return Response({'msg': 'Validation Error'})
from django.shortcuts import render

# Create your views here.
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User_Profile


def home(request):
    return JsonResponse({"message": "Hotel Management API is running 🚀"})

@csrf_exempt
def register(request):
    if request.method == "POST":
        data = json.loads(request.body)

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role")

        # ✅ Check if user already exists
        if User_Profile.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already taken"}, status=400)

        if User_Profile.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already registered"}, status=400)

        # ✅ Create user
        user = User_Profile.objects.create(
            username=username,
            email=email,
            password=make_password(password),  # hash password
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            phone=data.get("phone", ""),
            role=data.get("role", ""),
        )

        # ✅ Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return JsonResponse({

            "message": "User registered successfully",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            "tokens": {
                "refresh": str(refresh),
                "access": access_token,
            }
        }, status=201)


from django.contrib.auth.hashers import check_password
@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)

        username = data.get("username")
        password = data.get("password")

        try:
            # ✅ Get user by username
            user = User_Profile.objects.get(username=username)
        except User_Profile.DoesNotExist:
            return JsonResponse({"error": "Invalid username or password"}, status=400)

        # ✅ Check password
        if not check_password(password, user.password):
            return JsonResponse({"error": "Invalid username or password"}, status=400)

        # ✅ Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return JsonResponse({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            "tokens": {
                "refresh": str(refresh),
                "access": access_token,
            }
        }, status=200)


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@csrf_exempt
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update(request):    
    if request.method == "PUT":
        # ✅ Authenticate user using JWT
        jwt_authenticator = JWTAuthentication()
        try:
            user_auth_tuple = jwt_authenticator.authenticate(request)
            if user_auth_tuple is None:
                raise AuthenticationFailed("Authentication failed")
            user, token = user_auth_tuple
        except AuthenticationFailed as e:
            return JsonResponse({"error": str(e)}, status=401)

        data = json.loads(request.body)

        # ✅ Find user in your custom model
        try:
            user_profile = User_Profile.objects.get(id=user.id)
        except User_Profile.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        # ✅ Update fields (only if provided)
        user_profile.first_name = data.get("first_name", user_profile.first_name)
        user_profile.last_name = data.get("last_name", user_profile.last_name)
        user_profile.phone = data.get("phone", user_profile.phone)
        user_profile.email = data.get("email", user_profile.email)

        user_profile.save()

        return JsonResponse({
            "message": "User updated successfully",
            "user": {
                "id": user_profile.id,
                "username": user_profile.username,
                "email": user_profile.email,
                "first_name": user_profile.first_name,
                "last_name": user_profile.last_name,
                "phone": user_profile.phone,
            }
        }, status=200)

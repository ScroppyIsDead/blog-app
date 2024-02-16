import json
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def register(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password1 = data.get('password1')
            email = data.get('email')
            password2 = data.get('password2')

            if password1 == password2:

                user = User.objects.create_user(username=username, password=password1, email=email)

                return JsonResponse({"message": "sucessfully created user"})
            return JsonResponse({"message": "passwords don't match"})
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON format"})
    else:
        return JsonResponse({"success": False, "message": "Invalid request method"})
    
def userlogin(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")
            if username and password:
                user = authenticate(request=request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return JsonResponse({"message": "Successfully logged in"})
                
                return JsonResponse({"message": "Incorrect Username or Password"}, status=401)
            return JsonResponse({"message": "Username and password are required"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON format"}, status=400)
    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)

def getuserinformation(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            username = request.user.username
            return JsonResponse({"message": username})
        else: 
            return JsonResponse({"message": "User is not authenticated"}, status=401)
        
def userlogout(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({"message": "user logged out succesffully"})
        return JsonResponse({"message": "user no auth"})
    return JsonResponse({"message": "Data type Invalid"}, status=401)

@ensure_csrf_cookie
def get_csfr_token(request):
    return JsonResponse({"csrfToken": get_token(request)})
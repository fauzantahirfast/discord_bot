from django.shortcuts import render 
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
import requests
import jwt
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import DiscordAccountSerializer
from django.core.exceptions import ValidationError
import json
from rest_framework.parsers import JSONParser
from .models import UserAccountDetails
from django.core.exceptions import ObjectDoesNotExist
from .serializers import CustomTokenSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


auth_url_login = "https://discord.com/oauth2/authorize?client_id=1319769497552420884&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Foauth2%2Flogin%2Fredirect&scope=identify"
API_ENDPOINT = 'https://discord.com/api/v10'
CLIENT_ID = '1319769497552420884'
CLIENT_SECRET = 'PIbTCU71AjBsX31gKcLotc7Dxs_LwAIb'
REDIRECT_URI = 'http://localhost:8000/oauth2/login/redirect'  #smae in discord app that to redirect from discord code page to our website this to redirect from discord token page to website

# we go to /login route mapped with discord_login view ---> redirects to discord authorize page  --->  discord redirects to /oauth2/login/redirect with code in query param  ---> we map discord_login_redirect to redirect url get query param then send request for token and then with token request for details 



# in urls any parrametre passed like <int:id> should be given as a param to the view mapped to that view
def discord_login(request):
    return redirect(auth_url_login)


@api_view(['GET'])  #user is accessing details from server and wnats json displayyed on web doesnt matter if i am getting code from query param post requires user to submmit some info
def discord_login_redirect(request):
    data = request.query_params.get('code')  #gets code from query param
    user = exchange_code_for_token(data)  #passes code to exchange code which is gonna first exchange code for access token and then exchange token for user details
    serializer = DiscordAccountSerializer(user)
    data = {
    "username": user.username,
    "user_id": user.id
    }
    jwt_token= requests.post("http://localhost:8000/token/", data=data)
    jwt_token = jwt_token.json()
    print(jwt_token)
    jwt_token = json.dumps(jwt_token)
    print(jwt_token)
    frontend_redirect_url = f"http://localhost:5173/authcallback/?token={jwt_token}"
    return redirect(frontend_redirect_url)

def exchange_code_for_token(code):
    data = {
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': REDIRECT_URI, 
    'scope': 'identify'  #only for identification of user not more details guilds for getting server details
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    r = requests.post('https://discord.com/api/oauth2/token', data=data, headers= headers, auth=(CLIENT_ID, CLIENT_SECRET))  #requests the access and refresh token by passing code 
    credentials = r.json()
    access_token = credentials['access_token']
    user_details = exchange_token_for_details(access_token)
    return user_details
"""
EXCHANGES TOKEN FOR DETAILS
"""



def exchange_token_for_details(token): 
    res = requests.get("https://discord.com/api/v10/users/@me", headers={'Authorization': 'Bearer %s' % token})  #requests the user identification details by proving the access token in the header of the request
    user_data = res.json()
    try:
        # Check if the ID exists in the database
        existing_instance = UserAccountDetails.objects.get(id=user_data['id'])
        serializer = DiscordAccountSerializer(existing_instance, data=user_data)  # Pass instance for update
        if serializer.is_valid():
            updated_instance = serializer.save()
            print("Updated instance:", updated_instance)
            return updated_instance
        else:
            print("Validation errors:", serializer.errors)
            raise ValidationError(serializer.errors)
    except ObjectDoesNotExist:
        # If not found, create a new instance
        serializer = DiscordAccountSerializer(data=user_data)
        if serializer.is_valid():
            new_instance = serializer.save()
            print("Created new instance:", new_instance)
            return new_instance
        else:
            print("Validation errors:", serializer.errors)
            raise ValidationError(serializer.errors)


class CustomTokenView(APIView):
    def post(self, request):
        serializer = CustomTokenSerializer(data=request.data)


        if serializer.is_valid():
            # Extract username and ID
            username = serializer.validated_data['username']
            user_id = serializer.validated_data['user_id']
            
            # You can add logic here to verify the user if needed (e.g., check if the user exists)
            # For now, we'll assume the username and ID are valid
            user = UserAccountDetails.objects.get(id=user_id, username=username)

            # Create the JWT token
            refresh = RefreshToken.for_user(user)  # Ensure the `user` object is correctly retrieved by username and ID

            # Return the token
            return Response({
                'refresh': str(refresh),
        'access': str(refresh.access_token)})
            # return refresh
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home(request):
    user = request.user  # Access the user making the request
    return Response({
        "username": user.username,
        "email": user.email,
        # Any other user-related data
    })
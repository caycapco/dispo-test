from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
#from google.cloud.dialogflow_v2 import dialogflow_v2 as dialogflow
import os
#from google.cloud import dialogflow
import google.cloud.dialogflow_v2 as dialogflow
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from core.serializers import FacilitySerializer
from core.models import Facility
from django.db.models.functions import Radians, Power, Sin, Cos, ATan2, Sqrt, Radians
from django.db.models.expressions import RawSQL



def index(request):
    print("asd")
    return HttpResponse("Hey there :)")

@csrf_exempt
def webhook(request):
    
    if (request.method == 'POST'):

        print('Received a post request')

        body_unicode = request.body.decode('utf-8')
        req = json.loads(body_unicode)

        action = req.get('queryResult').get('action')
        print(action)

        #get currently logged-in user
        #User = get_user_model()
        #print(request.user.fullname)
        #user_name = request.user.fullname

        if(action == 'input.welcome'):
            message = "Hi, I'm Dispo. How may I help you today?"
            responseObj = {
                "fulfillmentText":  message,
                # "fulfillmentMessages": [{"text": {"text": [message]}}],
                "source": ""
            }

        print(responseObj)

        return JsonResponse(responseObj)

    return HttpResponse('OK')

def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        return response.query_result

@csrf_exempt
def send_message(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    message = body['message']

    #dialogflow detect intent
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    print(project_id)
    query_result = detect_intent_texts(project_id, "unique", message, 'en')
    
    #get current user based onn token
    token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
    current_user = get_user_from_access_token(token)
    print('current user fullname: ', current_user.firstName)

    #if query_result.action == "input.welcome":
    #    message = "Hi ", current_user.firstName,", I'm Dispo. How may I help you today?"
    #    response_text = { "message": message}

    #Check if intent.displayName = NearestLocation
    #if nearestLocation then get lat long and return list of nearest facility
    if query_result.intent.display_name == "NearestLocation":
        latitude = body['latitude']
        longitude = body['longitude'] 
        nearestFacilities = get_locations_nearby_coords(latitude, longitude)
        response_text = { "message":  query_result.fulfillment_text, "facility": nearestFacilities }
    else:
        response_text = { "message":  query_result.fulfillment_text}
    return JsonResponse(response_text)

def get_user_from_access_token(access_token_str):
    access_token_obj = AccessToken(access_token_str)
    user_id=access_token_obj['user_id']
    User = get_user_model()
    user=User.objects.get(id=user_id)
    #content =  {'user_id': user_id, 'user':user, 'user.id':user.id}
    #return Response(content)
    return user

def get_locations_nearby_coords(latitude, longitude):
    gcd_formula = "6371 * acos(least(greatest(cos(radians(%s)) * cos(radians(latitude)) \
    * cos(radians(longitude) - radians(%s)) + sin(radians(%s)) * sin(radians(latitude)) , -1), 1))"

    distance_raw_sql = RawSQL(gcd_formula,(latitude, longitude, latitude))
    qs = Facility.objects.all().annotate(distance=distance_raw_sql).order_by('distance')
    print('locs:', qs)
    serializer = FacilitySerializer(qs, many=True)
    #return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    return serializer.data
   
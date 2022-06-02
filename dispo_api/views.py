from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
#from google.cloud.dialogflow_v2 import dialogflow_v2 as dialogflow
import os
#from google.cloud import dialogflow
import google.cloud.dialogflow_v2 as dialogflow

@csrf_exempt
def webhook(request):
    
    if (request.method == 'POST'):

        print('Received a post request')

        body_unicode = request.body.decode('utf-8')
        req = json.loads(body_unicode)

        action = req.get('queryResult').get('action')
        print(action)

        if (action == 'search_world'): 

            apiCall = requests.get('https://covid19.mathdro.id/api').json()

            data = {
                'confirmed': apiCall['confirmed']['value'],
                'deaths': apiCall['deaths']['value'],
                'recovered': apiCall['recovered']['value']
            }

            message = "Total number of people in the world affected with COVID19 is {}. There have been {} deaths and {} people recovered.".format(format(data['confirmed'], ',d'), format(data['deaths'], ',d'), format(data['recovered'], ',d'))

            response = ""

            responseObj = {
                "fulfillmentText":  message,
                # "fulfillmentMessages": [{"text": {"text": [message]}}],
                "source": ""
            }

        elif (action == 'test'): 
            responseObj = {
                "fulfillmentText":  "test",
                # "fulfillmentMessages": [{"text": {"text": [message]}}],
                "source": ""
            }

        else:
            country = req.get('queryResult').get('parameters').get('geo-country')
            if (country == 'United States'):
                country = 'US'

            apiCall = requests.get("https://covid19.mathdro.id/api/countries/"+ country).json()

            data = {
                'confirmed': apiCall['confirmed']['value'],
                'deaths': apiCall['deaths']['value'],
                'recovered': apiCall['recovered']['value']
            }

            message = "Total number of people in {} affected with COVID19 is {}. There have been {} deaths and {} people recovered.".format(country, format(data['confirmed'], ',d'), format(data['deaths'], ',d'), format(data['recovered'], ',d'))
            response = ""

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
        return response.query_result.fulfillment_text

@csrf_exempt
def send_message(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    message = body['message']
    print(message)
    #message = request.form['message']
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    print(project_id)
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    response_text = { "message":  fulfillment_text }
    #response_text = { "message":  "here" }
    return JsonResponse(response_text)
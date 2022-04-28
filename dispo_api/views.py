from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json

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
from django.shortcuts import render
#from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class ChatView(APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'head', 'post']

    #@api_view(['GET'])
    def get(self, request):
    	text = request.query_params.get('text', '')
    	return Response({'message': 'Hello World! Your message is ' + text })
		#return JsonResponse({
		#	'message': 'Hello World!'
		#})


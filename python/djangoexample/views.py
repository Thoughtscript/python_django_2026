from django.shortcuts import render
from .models import Example, SubExample
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

def index(request):
    return render(request, 'index.html', {})

def all_examples(request):
    scan = Example.objects.all()
    response_data = {}
    response_data['data'] = serializers.serialize('json', scan)
    response_data['status'] = 200
    return JsonResponse(response_data)

def all_sub_examples(request):
    scan = SubExample.objects.all()
    response_data = {}
    response_data['data'] = serializers.serialize('json', scan)
    response_data['status'] = 200
    return JsonResponse(response_data)

@csrf_exempt
# Just for testing
def post_example(request):
    response_data = {}
    if request.method == "POST":
        json_body = json.loads(request.body)

        example = Example()
        example.name = json_body.get("name")
        example.save()

        response_data['data'] = '{ "name":' + example.name + '}'
        response_data['status'] = 200

    else:
        response_data['data'] = "Wrong Request Method Sent!"
        response_data['status'] = 401

    return JsonResponse(response_data)
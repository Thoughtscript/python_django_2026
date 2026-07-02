from django.shortcuts import render
from .models import Example, SubExample
from django.http import JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.views.decorators.cache import cache_page
import asyncio
import json

@cache_page(3600)
def index(request):
    return render(request, 'index.html', {})

def all_examples(request):
    response_data = {}
    if request.method == "GET":
        scan = Example.objects.all()
        response_data['data'] = serializers.serialize('json', scan)
        response_data['status'] = 200

    else:
        response_data['data'] = "Wrong Request Method Sent!"
        response_data['status'] = 401

    return JsonResponse(response_data, json_dumps_params={'indent': 4})

def all_sub_examples(request):
    response_data = {}
    if request.method == "GET":
        scan = SubExample.objects.all()
        response_data['data'] = serializers.serialize('json', scan)
        response_data['status'] = 200

    else:
        response_data['data'] = "Wrong Request Method Sent!"
        response_data['status'] = 401

    return JsonResponse(response_data, json_dumps_params={'indent': 4})

def disjoint_self(request):
    response_data = {}
    if request.method == "GET":
        try:
            raw_query = request.META.get('QUERY_STRING')
            query_dict = QueryDict(raw_query).dict()
            name_query_param = query_dict.get('name')
            sub_example = SubExample.objects.all().filter(name=name_query_param).first()
            disjoint_result = sub_example.disjoint_self
            response_data['data'] = serializers.serialize('json', disjoint_result)
            response_data['status'] = 200

        except Exception as ex:
            print(ex)
            response_data['data'] = "Error Encountered"
            response_data['status'] = 500

    else:
        response_data['data'] = "Wrong Request Method Sent!"
        response_data['status'] = 401

    return JsonResponse(response_data, json_dumps_params={'indent': 4})

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

    return JsonResponse(response_data, json_dumps_params={'indent': 4})
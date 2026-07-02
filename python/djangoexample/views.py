from django.shortcuts import render
from .models import Example, SubExample
from django.http import JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from asgiref.sync import async_to_sync
from django.core import serializers
import asyncio
import json

@cache_page(3600)
def index(request):
    return render(request, 'index.html', {})

'''
Allows this to be called from non async contexts

More powerful than asyncio alone:
runs the async function in a new sub-thread
supports threadlocals and thread_sensitive (running all thread_sensitive=True on the same but new thread)
https://docs.djangoproject.com/en/6.0/topics/async/#async-to-sync
'''
@async_to_sync 
async def one_example(request):
    response_data = {}
    if request.method == "GET":
        try:
            raw_query = request.META.get('QUERY_STRING')
            query_dict = QueryDict(raw_query).dict()
            pk_query_param = query_dict.get('pk')

            example = await Example.objects.aget(pk=pk_query_param)
            # if not found will throw
            response_data['data'] = { "pk": str(example.id), "name": example.name }
            response_data['status'] = 200

        except Exception as ex:
            print(ex)
            response_data['data'] = "Error Encountered"
            response_data['status'] = 500

    else:
        response_data['data'] = "Wrong Request Method Sent!"
        response_data['status'] = 401

    # Allows data structures beyond Dicts to be returned as JSON
    return JsonResponse(response_data, json_dumps_params={'indent': 4}, safe=False)

# synchronous
def all_examples(request):
    response_data = {}
    if request.method == "GET":
        scan = Example.objects.all()
        response_data['data'] = json.loads(serializers.serialize('json', scan))
        response_data['status'] = 200

    else:
        response_data['data'] = "Wrong Request Method Sent!"
        response_data['status'] = 401

    return JsonResponse(response_data, json_dumps_params={'indent': 4}, safe=False)

# async
async def all_sub_examples(request):
    response_data = {}
    if request.method == "GET":
        # don't await
        ## lazy - ensure necessary complex relationships are 'prefetch_related'
        ## or 'selected_related'
        scan = [sub_example async for sub_example in SubExample.objects.all()]
        response_data['data'] = json.loads(serializers.serialize('json', scan))
        response_data['status'] = 200

    else:
        response_data['data'] = "Wrong Request Method Sent!"
        response_data['status'] = 401

    return JsonResponse(response_data, json_dumps_params={'indent': 4}, safe=False)

# caches on first access
## each subsequent request will remove if in cache and retrieve
### regenerates at len 0
def disjoint_and_down_remove(request):
    response_data = {}
    if request.method == "GET":
        try:
            raw_query = request.META.get('QUERY_STRING')
            query_dict = QueryDict(raw_query).dict()
            name_query_param = query_dict.get('name')

            sub_example = SubExample.objects.all().filter(name=name_query_param).first()
            # if not found will not throw
            ## is None Type .exists() can't be called here
            if sub_example is not None:
                disjoint_result = sub_example.disjoint_and_down_remove

                # regenerate cache
                if len(disjoint_result) < 1:
                    del sub_example.disjoint_and_down_remove
                    disjoint_result = sub_example.disjoint_and_down_remove

                response_data['data'] = json.loads(serializers.serialize('json', disjoint_result))
                response_data['status'] = 200

            else:
                response_data['data'] = "Item Not Found!"
                response_data['status'] = 400
        
        except Exception as ex:
            print(ex)
            response_data['data'] = "Error Encountered"
            response_data['status'] = 500

    else:
        response_data['data'] = "Wrong Request Method Sent!"
        response_data['status'] = 401

    return JsonResponse(response_data, json_dumps_params={'indent': 4}, safe=False)

@csrf_exempt
# Just for testing
def post_example(request):
    response_data = {}
    if request.method == "POST":
        json_body = json.loads(request.body)

        example = Example()
        example.name = json_body.get("name")
        example.save()

        response_data['data'] = { "pk": str(example.id), "name": example.name }
        response_data['status'] = 201

    else:
        response_data['data'] = "Wrong Request Method Sent!"
        response_data['status'] = 401

    return JsonResponse(response_data, json_dumps_params={'indent': 4}, safe=False)


@csrf_exempt
# Just for testing
async def put_sub_example(request):
    response_data = {}
    if request.method == "PUT":
        try:
            raw_query = request.META.get('QUERY_STRING')
            query_dict = QueryDict(raw_query).dict()
            sub_example_pk = query_dict.get('sub_example_pk')
            example_pk = query_dict.get('example_pk')

            sub_example = await SubExample.objects.aget(pk=sub_example_pk)
            # if not found will throw
            example = await Example.objects.aget(pk=example_pk)
            sub_example.example = example
            await sub_example.asave()

            response_data['data'] = { "pk": str(sub_example.id), "name": sub_example.name, "example": { "pk": str(example.id), "name": example.name } }
            response_data['status'] = 201

        except Exception as ex:
            print(ex)
            response_data['data'] = "Error Encountered"
            response_data['status'] = 500

    else:
        response_data['data'] = "Wrong Request Method Sent!"
        response_data['status'] = 401

    return JsonResponse(response_data, json_dumps_params={'indent': 4}, safe=False)

# async
@csrf_exempt
# Just for testing
async def post_sub_example(request):
    response_data = {}
    if request.method == "POST":
        json_body = json.loads(request.body)

        subexample = SubExample()
        subexample.name = json_body.get("name")
        await subexample.asave()

        response_data['data'] = { "pk": str(subexample.id), "name": subexample.name }
        response_data['status'] = 201

    else:
        response_data['data'] = "Wrong Request Method Sent!"
        response_data['status'] = 401

    return JsonResponse(response_data, json_dumps_params={'indent': 4}, safe=False)

@csrf_exempt
# Just for testing
async def delete_many(request):
    response_data = {}
    if request.method == "DELETE":
        try:
            json_body = json.loads(request.body)
            to_delete = json_body.get('names_to_delete', [])
            count, _ = await Example.objects.filter(name__in=to_delete).adelete()
            response_data['data'] = { "deleted": str(count) }
            response_data['status'] = 200

        except Exception as ex:
            print(ex)
            response_data['data'] = "Error Encountered"
            response_data['status'] = 500

    else:
        response_data['data'] = "Wrong Request Method Sent!"
        response_data['status'] = 401

    return JsonResponse(response_data, json_dumps_params={'indent': 4}, safe=False)
from django.shortcuts import render
from .models import Example, SubExample
from django.http import JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from asgiref.sync import async_to_sync
from django.core import serializers
import asyncio
import json

# Still no private methods
## This is private by convention
def _make_json_response(data, status_code):
    # Allows data structures beyond Dicts to be returned as JSON
    ## This is status not status_code
    return JsonResponse(data, status=status_code, json_dumps_params={'indent': 4}, safe=False)

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
            
        except Exception as ex:
            print(ex)
            return _make_json_response("Error Encountered", 500)

    else:
        return _make_json_response("Wrong Request Method Sent", 401)

    return _make_json_response({ "pk": example.id, "name": example.name }, 200)

# synchronous
def all_examples(request):
    response_data = {}
    if request.method == "GET":
        scan = Example.objects.all()
        return _make_json_response(json.loads(serializers.serialize('json', scan)), 200)

    return _make_json_response("Wrong Request Method Sent", 401)

# async
async def all_sub_examples(request):
    response_data = {}
    if request.method == "GET":
        # don't await
        ## lazy - ensure necessary complex relationships are 'prefetch_related'
        ## or 'selected_related'
        scan = [sub_example async for sub_example in SubExample.objects.all()]
        return _make_json_response(json.loads(serializers.serialize('json', scan)), 200)

    return _make_json_response("Wrong Request Method Sent", 401)

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

                return _make_json_response(json.loads(serializers.serialize('json', disjoint_result)), 200)

            else:
                return _make_json_response("Item Not Found!", 400)
        
        except Exception as ex:
            print(ex)
            return _make_json_response("Error Encountered", 500)

    return _make_json_response("Wrong Request Method Sent", 401)

@csrf_exempt
# Just for testing
def post_example(request):
    response_data = {}
    if request.method == "POST":
        json_body = json.loads(request.body)

        example = Example()
        example.name = json_body.get("name")
        example.save()

        return _make_json_response({ "pk": example.id, "name": example.name }, 201)

    return _make_json_response("Wrong Request Method Sent", 401)


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

            return _make_json_response({ "pk": sub_example.id, "name": sub_example.name, "example": { "pk": example.id, "name": example.name } }, 201)

        except Exception as ex:
            print(ex)
            return _make_json_response("Error Encountered", 500)

    return _make_json_response("Wrong Request Method Sent", 401)

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

        return _make_json_response({ "pk": subexample.id, "name": subexample.name }, 201)

    return _make_json_response("Wrong Request Method Sent", 401)

@csrf_exempt
# Just for testing
async def delete_many(request):
    response_data = {}
    if request.method == "DELETE":
        try:
            json_body = json.loads(request.body)
            to_delete = json_body.get('names_to_delete', [])
            count, _ = await Example.objects.filter(name__in=to_delete).adelete()
    
            return _make_json_response({ "deleted": str(count) }, 200)

        except Exception as ex:
            print(ex)
            return _make_json_response("Error Encountered", 500)

    return _make_json_response("Wrong Request Method Sent", 401)
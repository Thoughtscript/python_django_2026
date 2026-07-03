from djangoexample.models import Example, SubExample
from django.http import JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import asyncio
import json

# Still no private methods
## This is private by convention
def _make_json_response(data, status_code):
    # Allows data structures beyond Dicts to be returned as JSON
    ## This is status not status_code
    return JsonResponse(data, status=status_code, json_dumps_params={'indent': 4}, safe=False)

async def all_sub_examples_service(request):
    response_data = {}
    if request.method == "GET":
        # don't await
        ## lazy - ensure necessary complex relationships are 'prefetch_related'
        ## or 'selected_related'
        scan = [sub_example async for sub_example in SubExample.objects.all()]
        return _make_json_response(json.loads(serializers.serialize('json', scan)), 200)

def disjoint_and_down_remove_service(request):
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

async def put_sub_example_service(request):
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

async def post_sub_example_service(request):
    response_data = {}
    if request.method == "POST":
        json_body = json.loads(request.body)

        subexample = SubExample()
        subexample.name = json_body.get("name")
        await subexample.asave()

        return _make_json_response({ "pk": subexample.id, "name": subexample.name }, 201)

    return _make_json_response("Wrong Request Method Sent", 401)
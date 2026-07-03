from django.http import JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.core.paginator import Paginator
from djangoexample.tasks.example import log_note
from djangoexample.models import Example, SubExample
import asyncio
import json

# Still no private methods
## This is private by convention
def _make_json_response(data, status_code):
    # Allows data structures beyond Dicts to be returned as JSON
    ## This is status not status_code
    return JsonResponse(data, status=status_code, json_dumps_params={'indent': 4}, safe=False)

async def one_example_service(request):
    response_data = {}
    if request.method == "GET":
        try:
            raw_query = request.META.get('QUERY_STRING')
            query_dict = QueryDict(raw_query).dict()
            pk_query_param = query_dict.get('pk')

            # Submit Task
            log_task = log_note.enqueue(msg = f"Example pk requested: {pk_query_param}")

            example = await Example.objects.aget(pk=pk_query_param)
            # If not found will throw

            # Get result of the above Task
            print(f"Task return_value: {log_task.return_value} status: {log_task.status}")
            
        except Exception as ex:
            print(ex)
            return _make_json_response("Error Encountered", 500)

    else:
        return _make_json_response("Wrong Request Method Sent", 401)

    return _make_json_response({ "pk": example.id, "name": example.name }, 200)

def post_example_service(request):
    response_data = {}
    if request.method == "POST":
        json_body = json.loads(request.body)

        example = Example()
        example.name = json_body.get("name")
        example.save()

        return _make_json_response({ "pk": example.id, "name": example.name }, 201)

    return _make_json_response("Wrong Request Method Sent", 401)

async def delete_many_examples_service(request):
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

def all_examples_service(request):
    response_data = {}
    if request.method == "GET":
        try:
            page_param = request.GET.get('page', 1) 

            ordered_scan = Example.objects.all().order_by('pk')
            paginator = Paginator(ordered_scan, 10)
            # Inbuilt fallback
            current_page = paginator.get_page(page_param)

            return _make_json_response({ "requested_page": page_param, "page": current_page.number, "page_data": json.loads(serializers.serialize('json', list(current_page.object_list))) }, 200)
        except Exception as ex:
            print(ex)
            return _make_json_response("Error Encountered", 500)

    return _make_json_response("Wrong Request Method Sent", 401)
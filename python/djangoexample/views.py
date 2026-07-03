from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from asgiref.sync import async_to_sync
from .services.example import one_example_service, post_example_service, delete_many_examples_service, all_examples_service
from .services.subexample import all_sub_examples_service, disjoint_and_down_remove_service, put_sub_example_service, post_sub_example_service
import asyncio

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
    return await one_example_service(request)

@csrf_exempt
# Just for testing
def post_example(request):
    return post_example_service(request)

# synchronous example
def all_examples(request):
    return all_examples_service(request)

@csrf_exempt
# Just for testing
async def delete_many_examples(request):
    return await delete_many_examples_service(request)

# async example
async def all_sub_examples(request):
    return await all_sub_examples_service(request)

# caches on first access
## each subsequent request will remove if in cache and retrieve
### regenerates at len 0
def disjoint_and_down_remove(request):
    return disjoint_and_down_remove_service(request)

@csrf_exempt
# Just for testing
async def put_sub_example(request):
    return await put_sub_example_service(request)

# async
@csrf_exempt
# Just for testing
async def post_sub_example(request):
    return await post_sub_example_service(request)

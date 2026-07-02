"""
URL configuration for djangoexample project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import index, all_sub_examples, all_examples, post_example
from django.views import debug

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', debug.default_urlconf), # Default Django view preserved

    # http://localhost:8000/test
    ## Don't include slash as in /test -> test
    path('test', index, name='index'),

    path('api/subexamples', all_sub_examples),

    path('api/examples', all_examples),

    path('api/examples/create', post_example),
]
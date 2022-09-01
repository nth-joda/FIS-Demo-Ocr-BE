from http.client import HTTPResponse
from urllib import response
from django.shortcuts import render

# Create your views here.


def index(request):
    response = HTTPResponse()
    response.write(b'Hello World')
    return response


def error(request, *args, **argv):
    return render(request, 'pages/error.html')

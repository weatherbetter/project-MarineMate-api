from django.shortcuts import render
from django.http import HttpRequest, JsonResponse

def index(request:HttpRequest):
    response = {'message' : "Hello world"}
    return JsonResponse(response)
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse("Hi this is from telebot app")

def run(request):
    return HttpResponse("Hi this is from telebot app in test function")

# from django.shortcuts import render
from django.http import HttpResponse

def index(request):
  return HttpResponse("hello, world. This is the patients index")

def detail(request, patient_id):
    return HttpResponse("You're viewing patient %s." % patient_id)

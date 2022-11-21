from django.shortcuts import render
from django.http import HttpResponse
import json


def index(request):
    json_data = json.loads(request.body)
    article = json_data['article']
    price = json_data['price']
    street = json_data['street']
    houseNr = json_data['houseNr']
    zipCode = json_data['zipCode']
    city = json_data['city']
    return HttpResponse(json_data['street'])
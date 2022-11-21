from django.shortcuts import render
from django.http import HttpResponse
import json


def index(request):
    json_data = json.loads(request.body)
    name = json_data['name']
    mail = json_data['mail']
    street = json_data['street']
    houseNr = json_data['houseNr']
    zipCode = json_data['zipCode']
    city = json_data['city']
    article = json_data['article']
    price = json_data['price']
    return HttpResponse(json_data['street'])
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers

from food.models import *

import json, decimal

# Create your views here.
@csrf_exempt
def test(request):
    return HttpResponse("hello")

@csrf_exempt
def FoodListView(request):
    food_list = Food.objects.all()
    food_list_serialized = []

    for food in food_list:

        food_obj = {}
        food_obj['name'] = food.name
        food_obj['description'] = food.description
        food_obj['price'] = str(food.price)
        food_obj['photo'] = food.name
        food_obj['is_halal'] = food.is_halal
        food_obj['is_vegan'] = food.is_vegan
        food_obj['is_liked'] = food.is_liked
        food_obj['cuisine'] = food.cuisine
        food_obj['restaurant'] = food.restaurant.name

        food_list_serialized.append(food_obj)

    return HttpResponse(json.dumps(food_list_serialized), content_type="application/json")
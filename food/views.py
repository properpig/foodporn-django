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
def FoodListView(request, username):
    food_list = Food.objects.all()
    food_list_serialized = []

    user = User.objects.get(username=username)

    for food in food_list:

        food_obj = {}
        food_obj['name'] = food.name
        food_obj['description'] = food.description
        food_obj['price'] = '${0:0.2f}'.format(food.price)

        food_obj['photo'] = food.photo
        food_obj['is_halal'] = food.is_halal
        food_obj['is_vegan'] = food.is_vegan
        food_obj['cuisine'] = food.cuisine
        food_obj['restaurant'] = food.restaurant.name

        food_obj['is_liked'] = food in user.foods_liked.all()
        food_obj['num_likes'] = User.objects.filter(foods_liked__in=[food]).count()

        food_list_serialized.append(food_obj)

    return HttpResponse(json.dumps(food_list_serialized), content_type="application/json")

@csrf_exempt
def LikedFoodListView(request, username):

    user = User.objects.get(username=username)

    food_list = user.foods_liked.all()
    food_list_serialized = []

    for food in food_list:

        food_obj = {}
        food_obj['name'] = food.name
        food_obj['description'] = food.description
        food_obj['price'] = '${0:0.2f}'.format(food.price)

        food_obj['photo'] = food.photo
        food_obj['is_halal'] = food.is_halal
        food_obj['is_vegan'] = food.is_vegan
        food_obj['cuisine'] = food.cuisine
        food_obj['restaurant'] = food.restaurant.name

        food_obj['num_likes'] = User.objects.filter(foods_liked__in=[food]).count()

        food_list_serialized.append(food_obj)

    return HttpResponse(json.dumps(food_list_serialized), content_type="application/json")
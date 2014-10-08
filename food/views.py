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
        food_obj['id'] = food.id
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
        food_obj['id'] = food.id
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

@csrf_exempt
def FollowingRestaurantsListView(request, username):

    user = User.objects.get(username=username)

    restaurants = user.restaurants_following.all()
    restaurants_list = []

    for restaurant in restaurants:

        restaurant_obj = {}
        restaurant_obj['name'] = restaurant.name
        restaurant_obj['location_name'] = restaurant.location_name
        restaurant_obj['photo'] = restaurant.photo
        restaurant_obj['price_low'] = '${0:0.0f}'.format(restaurant.price_low)
        restaurant_obj['price_high'] = '${0:0.0f}'.format(restaurant.price_high)

        restaurants_list.append(restaurant_obj)

    return HttpResponse(json.dumps(restaurants_list), content_type="application/json")

@csrf_exempt
def RecommendedRestaurantsListView(request, username):

    user = User.objects.get(username=username)

    user_restaurants_ids = [r.id for r in user.restaurants_following.all()]

    recommended_restaurants = Restaurant.objects.filter(is_recommended=True).exclude(id__in=user_restaurants_ids)
    restaurants_list = []

    for restaurant in recommended_restaurants:

        restaurant_obj = {}
        restaurant_obj['name'] = restaurant.name
        restaurant_obj['location_name'] = restaurant.location_name
        restaurant_obj['photo'] = restaurant.photo
        restaurant_obj['price_low'] = '${0:0.0f}'.format(restaurant.price_low)
        restaurant_obj['price_high'] = '${0:0.0f}'.format(restaurant.price_high)

        # get the people following this restaurant
        restaurant_obj['followed_by'] = [{'username': user.username, 'profile_pic': user.profile_pic} for user in User.objects.filter(restaurants_following__in=[restaurant])]
        restaurant_obj['following_count'] = len(restaurant_obj['followed_by'])

        restaurants_list.append(restaurant_obj)

    return HttpResponse(json.dumps(restaurants_list), content_type="application/json")

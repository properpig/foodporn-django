from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers

from food.models import *
from utils import timesince

import json, decimal, time

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
        restaurant_obj['id'] = restaurant.id
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

    recommended_restaurants = Restaurant.objects.filter(is_recommended=True)
    restaurants_list = []

    for restaurant in recommended_restaurants:

        restaurant_obj = {}
        restaurant_obj['name'] = restaurant.name
        restaurant_obj['id'] = restaurant.id
        restaurant_obj['location_name'] = restaurant.location_name
        restaurant_obj['photo'] = restaurant.photo
        restaurant_obj['price_low'] = '${0:0.0f}'.format(restaurant.price_low)
        restaurant_obj['price_high'] = '${0:0.0f}'.format(restaurant.price_high)

        # get the people following this restaurant
        restaurant_obj['followed_by'] = [{'user_id':user.id, 'username': user.username, 'profile_pic': user.profile_pic} for user in User.objects.filter(restaurants_following__in=[restaurant])[:7]]
        restaurant_obj['following_count'] = User.objects.filter(restaurants_following__in=[restaurant]).count()

        restaurant_obj['is_following'] = (restaurant.id in user_restaurants_ids)

        restaurants_list.append(restaurant_obj)

    return HttpResponse(json.dumps(restaurants_list), content_type="application/json")

@csrf_exempt
def DealsActivityListView(request):

    deals = DealsActivity.objects.all()
    deals_list = []

    for deal in deals:

        deal_obj = {}
        deal_obj['title'] = deal.title
        deal_obj['photo'] = deal.photo
        deal_obj['restaurant'] = deal.restaurant.name
        deal_obj['restaurant_id'] = deal.restaurant.id
        deal_obj['details'] = deal.details
        deal_obj['more'] = deal.more_details

        deals_list.append(deal_obj)

    return HttpResponse(json.dumps(deals_list), content_type="application/json")

@csrf_exempt
def FriendsActivityListView(request, username):

    activities = FriendsActivity.objects.all().order_by('-timestamp')
    activity_list = []

    for activity in activities:
        activity_obj = {}
        activity_obj['type'] = activity.activity_type
        activity_obj['timestamp'] = timesince(activity.timestamp)

        if activity.actor:
            activity_obj['actor'] = activity.actor.name
            activity_obj['actor_id'] = activity.actor.id
            activity_obj['actor_photo'] = activity.actor.profile_pic

        if activity.friend:
            activity_obj['friend'] = activity.friend.name
            activity_obj['friend_id'] = activity.friend.id
            activity_obj['friend_photo'] = activity.friend.profile_pic

        if activity.restaurant:
            activity_obj['restaurant'] = activity.restaurant.name
            activity_obj['restaurant_id'] = activity.restaurant.id
            activity_obj['restaurant_photo'] = activity.restaurant.photo

        if activity.review:
            activity_obj['actor'] = activity.review.user.name
            activity_obj['actor_id'] = activity.review.user.id
            activity_obj['actor_photo'] = activity.review.user.profile_pic
            activity_obj['restaurant'] = activity.review.restaurant.name
            activity_obj['restaurant_id'] = activity.review.restaurant.id
            activity_obj['restaurant_photo'] = activity.review.restaurant.photo
            activity_obj['photo'] = activity.review.photo
            activity_obj['rating'] = activity.review.rating

        if activity_obj['type'] == "achievement":
            activity_obj['foods'] = [{'food_photo': food.photo, 'food_id': food.id} for food in activity.actor.foods_liked.all()[:7]]

        activity_list.append(activity_obj)

    return HttpResponse(json.dumps(activity_list), content_type="application/json")



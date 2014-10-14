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
def FoodView(request, food_id, username):

    user = User.objects.get(username=username)
    food = Food.objects.get(id=food_id)

    food_obj = {}
    food_obj['name'] = food.name
    food_obj['photo'] = food.photo
    food_obj['restaurant'] = food.restaurant.name
    food_obj['restaurant_id'] = food.restaurant.id
    food_obj['description'] = food.description

    food_obj['num_likes'] = User.objects.filter(foods_liked__in=[food]).count()
    food_obj['liked_by'] = [{'user_id':user.id, 'photo': user.photo} for user in User.objects.filter(foods_liked__in=[food])[:7]]
    food_obj['is_liked'] = food in user.foods_liked.all()

    return HttpResponse(json.dumps(food_obj), content_type="application/json")

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
        restaurant_obj['followed_by'] = [{'user_id':user.id, 'username': user.username, 'photo': user.photo} for user in User.objects.filter(restaurants_following__in=[restaurant])[:7]]
        restaurant_obj['following_count'] = User.objects.filter(restaurants_following__in=[restaurant]).count()

        restaurant_obj['is_following'] = (restaurant.id in user_restaurants_ids)

        restaurants_list.append(restaurant_obj)

    return HttpResponse(json.dumps(restaurants_list), content_type="application/json")

@csrf_exempt
def RestaurantView(request, restaurant_id, username):

    user = User.objects.get(username=username)
    restaurant = Restaurant.objects.get(id=restaurant_id)

    restaurant_obj = {}
    restaurant_obj['name'] = restaurant.name
    restaurant_obj['photo'] = restaurant.photo
    restaurant_obj['description'] = restaurant.description
    restaurant_obj['price_low'] = '${0:0.0f}'.format(restaurant.price_low)
    restaurant_obj['price_high'] = '${0:0.0f}'.format(restaurant.price_high)
    restaurant_obj['location_name'] = restaurant.location_name

    restaurant_obj['telephone'] = restaurant.telephone
    restaurant_obj['email'] = restaurant.email
    restaurant_obj['opening_hours'] = restaurant.opening_hours

    restaurant_obj['followed_by'] = [{'user_id':user.id, 'username': user.username, 'photo': user.photo} for user in User.objects.filter(restaurants_following__in=[restaurant])[:7]]
    restaurant_obj['following_count'] = User.objects.filter(restaurants_following__in=[restaurant]).count()

    reviews = Review.objects.filter(restaurant__in=[restaurant])
    if reviews.count():
        rating = 0
        for review in reviews:
            rating = rating + review.rating
        rating = rating / reviews.count()
    else:
        rating = 0

    restaurant_obj['rating'] = rating
    restaurant_obj['reviews_count'] = reviews.count()
    restaurant_obj['reviews'] = [{'id': review.id, 'photo': review.photo} for review in reviews]

    restaurant_obj['foods'] = [{'id': food.id, 'photo': food.photo} for food in Food.objects.filter(restaurant=restaurant)]
    restaurant_obj['food_count'] = Food.objects.filter(restaurant=restaurant).count()

    deals = DealsActivity.objects.filter(restaurant__in=[restaurant])
    restaurant_obj['deals'] = [{'title': deal.title, 'photo': deal.photo, 'details': deal.details, 'more': deal.more_details} for deal in deals]

    return HttpResponse(json.dumps(restaurant_obj), content_type="application/json")

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
        deal_obj['description'] = deal.restaurant.id
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
            activity_obj['actor_photo'] = activity.actor.photo

        if activity.friend:
            activity_obj['friend'] = activity.friend.name
            activity_obj['friend_id'] = activity.friend.id
            activity_obj['friend_photo'] = activity.friend.photo

        if activity.restaurant:
            activity_obj['restaurant'] = activity.restaurant.name
            activity_obj['restaurant_id'] = activity.restaurant.id
            activity_obj['restaurant_photo'] = activity.restaurant.photo

        if activity.review:
            activity_obj['actor'] = activity.review.user.name
            activity_obj['actor_id'] = activity.review.user.id
            activity_obj['actor_photo'] = activity.review.user.photo
            activity_obj['restaurant'] = activity.review.restaurant.name
            activity_obj['restaurant_id'] = activity.review.restaurant.id
            activity_obj['restaurant_photo'] = activity.review.restaurant.photo
            activity_obj['photo'] = activity.review.photo
            activity_obj['rating'] = activity.review.rating

        if activity_obj['type'] == "achievement":
            activity_obj['foods'] = [{'food_photo': food.photo, 'food_id': food.id} for food in activity.actor.foods_liked.all()[:7]]

        activity_list.append(activity_obj)

    return HttpResponse(json.dumps(activity_list), content_type="application/json")

@csrf_exempt
def PeopleFollowingView(request, username):

    this_user = User.objects.get(username=username)
    following = this_user.following.all()
    following_list = []

    for user in following:
        user_obj = {}
        user_obj['id'] = user.id
        user_obj['name'] = user.name
        user_obj['photo'] = user.photo

        user_obj['num_likes'] = user.foods_liked.all().count()
        # user_obj['likes'] = [{'food_id': food.id, 'photo': food.photo} for food in user.foods_liked.all()[:5]]

        user_obj['num_followers'] = user.followers.all().count()

        user_obj['num_reviews'] = Review.objects.filter(user=user).count()
        user_obj['reviews'] = [{'restaurant_id': review.restaurant.id, 'photo': review.photo} for review in Review.objects.filter(user=user)[:5]]

        following_list.append(user_obj)

    return HttpResponse(json.dumps(following_list), content_type="application/json")

@csrf_exempt
def PeopleRecommendedView(request, username):

    this_user = User.objects.get(username=username)
    recommended = User.objects.filter(is_recommended=True)
    recommended_list = []

    for user in recommended:
        user_obj = {}
        user_obj['id'] = user.id
        user_obj['name'] = user.name
        user_obj['photo'] = user.photo
        user_obj['is_following'] = user in this_user.following.all()

        user_obj['num_likes'] = user.foods_liked.all().count()
        # user_obj['likes'] = [{'food_id': food.id, 'photo': food.photo} for food in user.foods_liked.all()[:5]]

        user_obj['num_followers'] = user.followers.all().count()

        user_obj['num_reviews'] = Review.objects.filter(user=user).count()
        user_obj['reviews'] = [{'restaurant_id': review.restaurant.id, 'photo': review.photo} for review in Review.objects.filter(user=user)[:5]]

        recommended_list.append(user_obj)

    return HttpResponse(json.dumps(recommended_list), content_type="application/json")

@csrf_exempt
def UserView(request, user_id, username):

    this_user = User.objects.get(username=username)
    user = User.objects.get(id=user_id)

    user_obj = {}
    user_obj['id'] = user.id
    user_obj['name'] = user.name
    user_obj['photo'] = user.photo
    user_obj['is_following'] = user in this_user.following.all()

    user_obj['num_likes'] = user.foods_liked.all().count()
    # user_obj['likes'] = [{'food_id': food.id, 'photo': food.photo} for food in user.foods_liked.all()[:5]]

    user_obj['num_followers'] = user.followers.all().count()
    user_obj['followers'] = [{'id': person.id, 'photo': person.photo} for person in user.followers.all()]

    user_obj['num_following'] = user.following.all().count()
    user_obj['following'] = [{'id': person.id, 'photo': person.photo} for person in user.following.all()]

    user_obj['num_reviews'] = Review.objects.filter(user=user).count()
    user_obj['reviews'] = [{'restaurant_id': review.restaurant.id, 'photo': review.photo} for review in Review.objects.filter(user=user)[:5]]

    return HttpResponse(json.dumps(user_obj), content_type="application/json")

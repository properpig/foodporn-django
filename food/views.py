from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from django.shortcuts import render
from django.http import HttpResponse, QueryDict, HttpResponseRedirect
from django.core import serializers

from food.models import *
from utils import timesince, unique, haversine
from md5 import md5

import json, decimal, time

# Create your views here.
@csrf_exempt
def test(request):
    return HttpResponse("hello")

@csrf_exempt
def LoginView(request):
    username = request.GET.get('username', False)
    code = request.GET.get('vcode', False)

    if (not username) or (not code):
        return HttpResponse(json.dumps({'error': 'please supply username and vcode'}), content_type="application/json")


    generated_code = md5(username+"food!").hexdigest()

    if (generated_code != code):
        return HttpResponse(json.dumps({'error': 'code is wrong'}), content_type="application/json")

    return HttpResponse(json.dumps({'success': 'foodie ' + username}), content_type="application/json")

@csrf_exempt
def UserNavView(request):
    username = request.GET.get('username', 'john') #defaults to john
    page = request.GET.get('page', '')
    try:
        user = User.objects.get(username=username)
    except:
        user = User.objects.get(username='john')

    # log the event
    event = Event(actor=user, ui_type='A', page=page, event_type='page visit')
    event.save()

    user_obj = {'id': user.id, 'name': user.name, 'photo': user.photo}
    return HttpResponse(json.dumps(user_obj), content_type="application/json")

@csrf_exempt
def FoodListView(request, username):

    food_list_serialized = []
    user = User.objects.get(username=username)

    food_list = Food.objects.all().select_related('user', 'restaurant', 'food')

    if request.GET.get('search', False):
        query_string = request.GET.get('search', False)
        food_list = food_list.filter(Q(name__icontains=query_string) | Q(description__icontains=query_string))
    if request.GET.get('liked', False):
        food_list = food_list.filter(foods_liked__in=[user]).order_by('-id')
    if request.GET.get('friends_like', False):
        friends = [u['id'] for u in user.following.values('id')]
        food_list = food_list.filter(foods_liked__in=friends).order_by('-id')
    if request.GET.get('recommended', False):
        restaurants = Restaurant.objects.filter(is_recommended=True)
        food_list = food_list.filter(restaurant__in=restaurants).order_by('-id')
    if request.GET.get('following', False):
        restaurants = Restaurant.objects.filter(restaurants_following__in=[user])
        food_list = food_list.filter(restaurant__in=restaurants).order_by('-id')
    if request.GET.get('friends_following', False):
        friends = user.following.all()
        restaurants = Restaurant.objects.filter(restaurants_following__in=friends)
        food_list = food_list.filter(restaurant__in=restaurants).order_by('-id')
    if request.GET.get('disliked', False):
        food_list = food_list.filter(foods_disliked__in=[user]).order_by('-id')
    if request.GET.get('explore', False):
        food_list = food_list.exclude(foods_liked__in=[user]).exclude(foods_disliked__in=[user]).order_by('id')
    if request.GET.get('dietary_ids', False):
        dietary_ids = request.GET.get('dietary_ids', False).split(',')
        food_list = food_list.filter(dietary__in=dietary_ids)
    if request.GET.get('cuisine_ids', False):
        cuisine_ids = request.GET.get('cuisine_ids', False).split(',')
        food_list = food_list.filter(cuisine__in=cuisine_ids)

    # filter by range
    if request.GET.get('price_max', False):
        price_max = request.GET.get('price_max', False)
        food_list = food_list.filter(price__lte=int(price_max))
    if request.GET.get('price_min', False):
        price_min = request.GET.get('price_min', False)
        food_list = food_list.filter(price__gte=int(price_min))

    distance_max = request.GET.get('distance_max', False)
    if distance_max:
        distance_max = float(distance_max)
    distance_min = request.GET.get('distance_min', False)
    if distance_min:
        distance_min = float(distance_min)

    #sorting by non-derived field
    sort = request.GET.get('sort', False)
    if sort == 'price':
        food_list = food_list.order_by('price')

    food_list = unique(food_list)

    for food in food_list:

        food_obj = {}
        food_obj['id'] = food.id
        food_obj['name'] = food.name
        # food_obj['description'] = food.description
        food_obj['price'] = '${0:0.2f}'.format(food.price)

        food_obj['dist'] = haversine(float(user.location_x), float(user.location_y), float(food.restaurant.location_x), float(food.restaurant.location_y))
        food_obj['distance'] = '{0:0.2f}km'.format(food_obj['dist'])

        # if a distance filter has been set, we only add qualifying restaurants
        if distance_max:
            if food_obj['dist'] > distance_max:
                continue
        if distance_min:
            if food_obj['dist'] < distance_min:
                continue

        food_obj['photo'] = food.photo
        food_obj['restaurant'] = food.restaurant.name
        food_obj['restaurant_id'] = food.restaurant.id
        food_obj['dietary_ids'] = [{'id':i.id, 'name':i.name} for i in food.dietary.all()]
        food_obj['cuisine_ids'] = [{'id':i.id, 'name':i.name} for i in food.cuisine.all()]

        food_obj['is_liked'] = food in user.foods_liked.all()
        food_obj['num_likes'] = User.objects.filter(foods_liked__in=[food]).count()

        food_list_serialized.append(food_obj)

    # sorting by derived field
    if sort == 'likes':
        food_list_serialized = sorted(food_list_serialized, key=lambda x: x['num_likes'], reverse=True)
    elif sort == 'location':
        food_list_serialized = sorted(food_list_serialized, key=lambda x: x['dist'])

    return HttpResponse(json.dumps(food_list_serialized), content_type="application/json")

@csrf_exempt
def FoodView(request, food_id, username):

    user = User.objects.get(username=username)
    food = Food.objects.get(id=food_id)

    food_obj = {}
    food_obj['name'] = food.name
    food_obj['photo'] = food.photo
    food_obj['price'] = '${0:0.2f}'.format(food.price)
    food_obj['restaurant'] = food.restaurant.name
    food_obj['restaurant_id'] = food.restaurant.id
    food_obj['description'] = food.description

    food_obj['num_likes'] = User.objects.filter(foods_liked__in=[food]).count()
    food_obj['less_than_8'] = food_obj['num_likes'] <= 7
    food_obj['liked_by'] = [{'user_id':person.id, 'photo': person.photo} for person in User.objects.filter(foods_liked__in=[food])[:6]]
    food_obj['is_liked'] = food in user.foods_liked.all()
    food_obj['is_disliked'] = food in user.foods_disliked.all()


    food_obj['cuisine'] = [{'name': cuisine.name, 'image': cuisine.image} for cuisine in food.cuisine.all().order_by('position')]
    food_obj['dietary'] = [{'name': diet.name, 'image': diet.image} for diet in food.dietary.all().order_by('position')]

    food_obj['menu'] = [{'id': f.id, 'photo': f.photo, 'name': f.name, 'price':'${0:0.2f}'.format(f.price), 'num_likes': User.objects.filter(foods_liked__in=[food]).count()} for f in Food.objects.filter(restaurant=food.restaurant)]

    return HttpResponse(json.dumps(food_obj), content_type="application/json")

@csrf_exempt
def FoodLikeView(request, food_id, username):

    user = User.objects.get(username=username)
    food = Food.objects.get(id=food_id)

    # log the event
    event = Event(actor=user, ui_type='A', event_type='like', swipe=request.GET.get('swipe', False))
    event.save()

    # history
    history = History(user=user, food=food)
    history.save()

    if user.foods_liked.filter(id=food.id):
        user.foods_liked.remove(food)

        user.save()
        return HttpResponse(json.dumps({'status': 'success'}), content_type="application/json")

    user.foods_liked.add(food)

    if user.foods_disliked.filter(id=food.id):
        user.foods_disliked.remove(food)

    user.save()

    return HttpResponse(json.dumps({'status': 'success'}), content_type="application/json")

@csrf_exempt
def FoodDislikeView(request, food_id, username):

    user = User.objects.get(username=username)
    food = Food.objects.get(id=food_id)

    # log the event
    event = Event(actor=user, ui_type='A', event_type='dislike', swipe=request.GET.get('swipe', False))
    event.save()

    # history
    history = History(user=user, food=food)
    history.save()

    if user.foods_disliked.filter(id=food.id):
        user.foods_disliked.remove(food)

        user.save()
        return HttpResponse(json.dumps({'status': 'success'}), content_type="application/json")

    user.foods_disliked.add(food)

    if user.foods_liked.filter(id=food.id):
        user.foods_liked.remove(food)

    user.save()

    return HttpResponse(json.dumps({'status': 'success'}), content_type="application/json")

@csrf_exempt
def FoodResetView(request, food_id, username):

    user = User.objects.get(username=username)
    food = Food.objects.get(id=food_id)

    # log the event
    event = Event(actor=user, ui_type='A', event_type='undo')
    event.save()

    # history
    history = History(user=user, food=food)
    history.save()

    if user.foods_disliked.filter(id=food.id):
        user.foods_disliked.remove(food)

    if user.foods_liked.filter(id=food.id):
        user.foods_liked.remove(food)

    user.save()

    return HttpResponse(json.dumps({'status': 'success'}), content_type="application/json")

@csrf_exempt
def FoodHistoryView(request, username):

    user = User.objects.get(username=username)
    history = History.objects.filter(user=user).order_by('-timestamp')

    food_list = []

    seen = set()
    unique_history = [x for x in history if x.food not in seen and not seen.add(x.food)]

    for item in unique_history:
        food = item.food

        food_obj = {}
        food_obj['id'] = food.id
        food_obj['name'] = food.name
        # food_obj['description'] = food.description
        food_obj['price'] = '${0:0.2f}'.format(food.price)

        food_obj['photo'] = food.photo
        food_obj['restaurant'] = food.restaurant.name
        food_obj['restaurant_id'] = food.restaurant.id

        food_obj['is_liked'] = food in user.foods_liked.all()
        food_obj['is_disliked'] = food in user.foods_disliked.all()
        food_obj['is_neither'] = (not food_obj['is_liked']) and (not food_obj['is_disliked'])
        food_obj['num_likes'] = User.objects.filter(foods_liked__in=[food]).count()

        food_obj['timestamp'] = item.timestamp.strftime("%b %d %H:%M:%S")

        food_list.append(food_obj)

    return HttpResponse(json.dumps(food_list), content_type="application/json")

@csrf_exempt
def RestaurantsListView(request, username):

    user = User.objects.get(username=username)
    user_restaurants_ids = [r.id for r in user.restaurants_following.all()]

    restaurants = Restaurant.objects.all().select_related('user', 'restaurant', 'food')
    restaurants_list = []

    if request.GET.get('search', False):
        query_string = request.GET.get('search', False)
        restaurants = restaurants.filter(Q(name__icontains=query_string) | Q(description__icontains=query_string) | Q(location_name__icontains=query_string))
    if request.GET.get('following', False):
        restaurants = restaurants.filter(restaurants_following__in=[user])
    if request.GET.get('friends_following', False):
        friends = [u['id'] for u in user.following.values('id')]
        restaurants = restaurants.filter(restaurants_following__in=friends)
    if request.GET.get('recommended', False):
        restaurants = restaurants.filter(is_recommended=True)
    if request.GET.get('me_like', False):
        resturant_ids = user.foods_liked.values('restaurant__id')
        seen = set()
        unique_rids = [r['restaurant__id'] for r in resturant_ids if r['restaurant__id'] not in seen and not seen.add(r['restaurant__id'])]
        restaurants = restaurants.filter(id__in=unique_rids)
    if request.GET.get('friends_like', False):
        resturant_ids = user.following.values('foods_liked__restaurant__id')
        seen = set()
        unique_rids = [r['foods_liked__restaurant__id'] for r in resturant_ids if r['foods_liked__restaurant__id'] not in seen and not seen.add(r['foods_liked__restaurant__id'])]
        restaurants = restaurants.filter(id__in=unique_rids)
    if request.GET.get('me_review', False):
        resturant_ids = Review.objects.filter(user=user).values('restaurant__id')
        seen = set()
        unique_rids = [r['restaurant__id'] for r in resturant_ids if r['restaurant__id'] not in seen and not seen.add(r['restaurant__id'])]
        restaurants = restaurants.filter(id__in=unique_rids)
    if request.GET.get('recommended_people_review', False):
        users = User.objects.filter(is_recommended=True)
        resturant_ids = Review.objects.filter(user__in=users).values('restaurant__id')
        seen = set()
        unique_rids = [r['restaurant__id'] for r in resturant_ids if r['restaurant__id'] not in seen and not seen.add(r['restaurant__id'])]
        restaurants = restaurants.filter(id__in=unique_rids)
    if request.GET.get('friends_review', False):
        friends = user.following.all()
        resturant_ids = Review.objects.filter(user__in=friends).values('restaurant__id')
        seen = set()
        unique_rids = [r['restaurant__id'] for r in resturant_ids if r['restaurant__id'] not in seen and not seen.add(r['restaurant__id'])]
        restaurants = restaurants.filter(id__in=unique_rids)
    if request.GET.get('amenity_ids', False):
        amenity_ids = request.GET.get('amenity_ids', False).split(',')
        restaurants = restaurants.filter(amenities__in=amenity_ids)
    if request.GET.get('dietary_ids', False):
        dietary_ids = request.GET.get('dietary_ids', False).split(',')
        food_ids = Food.objects.filter(dietary__in=dietary_ids)
        restaurants = restaurants.filter(food__in=food_ids)
    if request.GET.get('cuisine_ids', False):
        cuisine_ids = request.GET.get('cuisine_ids', False).split(',')
        food_ids = Food.objects.filter(cuisine__in=cuisine_ids)
        restaurants = restaurants.filter(food__in=food_ids)

    # filter by range
    if request.GET.get('price_max', False):
        price_max = request.GET.get('price_max', False)
        restaurants = restaurants.filter(price_high__lte=int(price_max))
    if request.GET.get('price_min', False):
        price_min = request.GET.get('price_min', False)
        restaurants = restaurants.filter(price_low__gte=int(price_min))

    distance_max = request.GET.get('distance_max', False)
    if distance_max:
        distance_max = float(distance_max)
    distance_min = request.GET.get('distance_min', False)
    if distance_min:
        distance_min = float(distance_min)

    #sorting by non-derived field
    sort = request.GET.get('sort', False)
    if sort == 'price':
        restaurants = restaurants.extra(select={'price_range': 'price_high + price_low'}).extra(order_by=['price_range'])

    # get distinct restaurants
    restaurants = unique(restaurants)

    for restaurant in restaurants:
        restaurant_obj = {}
        restaurant_obj['name'] = restaurant.name
        restaurant_obj['id'] = restaurant.id
        restaurant_obj['location_name'] = restaurant.location_name
        restaurant_obj['location'] = {'x':restaurant.location_x, 'y':restaurant.location_y}

        restaurant_obj['dist'] = haversine(float(user.location_x), float(user.location_y), float(restaurant.location_x), float(restaurant.location_y))
        restaurant_obj['distance'] = '{0:0.2f}km'.format(restaurant_obj['dist'])

        # if a distance filter has been set, we only add qualifying restaurants
        if distance_max:
            if restaurant_obj['dist'] > distance_max:
                continue
        if distance_min:
            if restaurant_obj['dist'] < distance_min:
                continue

        restaurant_obj['photo'] = restaurant.photo
        restaurant_obj['price_low'] = '${0:0.0f}'.format(restaurant.price_low)
        restaurant_obj['price_high'] = '${0:0.0f}'.format(restaurant.price_high)
        # restaurant_obj['amenities'] = [{'id': res.id, 'image': res.image} for res in restaurant.amenities.all()]


        # get the people following this restaurant
        restaurant_obj['followed_by'] = [{'user_id':person.id, 'username': person.username, 'photo': person.photo} for person in User.objects.filter(restaurants_following__in=[restaurant])[:7]]
        restaurant_obj['following_count'] = User.objects.filter(restaurants_following__in=[restaurant]).count()

        restaurant_obj['is_following'] = (restaurant.id in user_restaurants_ids)
        restaurant_obj['is_recommended'] = restaurant.is_recommended

        # ratings
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

        restaurants_list.append(restaurant_obj)

    # sorting by derived field
    if sort == 'followers':
        restaurants_list = sorted(restaurants_list, key=lambda x: x['following_count'], reverse=True)
    elif sort == 'location':
        restaurants_list = sorted(restaurants_list, key=lambda x: x['dist'])
    elif sort == 'ratings':
        restaurants_list = sorted(restaurants_list, key=lambda x: x['rating'])

    return HttpResponse(json.dumps(restaurants_list), content_type="application/json")

@csrf_exempt
def RestaurantView(request, restaurant_id, username):

    user = User.objects.get(username=username)
    restaurant = Restaurant.objects.get(id=restaurant_id)

    restaurant_obj = {}
    restaurant_obj['restaurant_id'] = restaurant.id
    restaurant_obj['name'] = restaurant.name
    restaurant_obj['photo'] = restaurant.photo
    restaurant_obj['description'] = restaurant.description
    restaurant_obj['price_low'] = '${0:0.0f}'.format(restaurant.price_low)
    restaurant_obj['price_high'] = '${0:0.0f}'.format(restaurant.price_high)
    restaurant_obj['location_name'] = restaurant.location_name
    restaurant_obj['location_x'] = restaurant.location_x
    restaurant_obj['location_y'] = restaurant.location_y

    restaurant_obj['telephone'] = restaurant.telephone
    restaurant_obj['email'] = restaurant.email
    restaurant_obj['opening_hours'] = restaurant.opening_hours

    restaurant_obj['amenities'] = [{'name': res.name, 'image': res.image} for res in restaurant.amenities.all()]
    restaurant_obj['amenities_count'] = len(restaurant_obj['amenities'])

    # get the cuisine type(s)
    cuisine_ids = restaurant.food_set.values('cuisine__id')
    cuisine_types = [{'name': cuisine.name, 'image': cuisine.image} for cuisine in Cuisine.objects.filter(id__in=cuisine_ids).order_by('position')]
    restaurant_obj['cuisine'] = cuisine_types

    # get dietary types
    dietary_ids = restaurant.food_set.values('dietary__id')
    dietary_types = [{'name': diet.name, 'image': diet.image} for diet in Diet.objects.filter(id__in=dietary_ids).order_by('position')]
    restaurant_obj['dietary'] = dietary_types

    restaurant_obj['is_following'] = restaurant in user.restaurants_following.all()
    restaurant_obj['followed_by'] = [{'user_id':user.id, 'username': user.username, 'photo': user.photo} for user in User.objects.filter(restaurants_following__in=[restaurant])[:7]]
    restaurant_obj['following_count'] = User.objects.filter(restaurants_following__in=[restaurant]).count()
    restaurant_obj['less_than_8'] = restaurant_obj['following_count'] <= 7

    restaurant_obj['is_recommended'] = restaurant.is_recommended

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
    restaurant_obj['reviews'] = [{'id': review.id, 'photo': review.photo, 'rating': review.rating, 'text': review.text, 'user':{'id': review.user.id, 'username': review.user.username, 'photo': review.user.photo}} for review in reviews]

    restaurant_obj['foods'] = [{'id': food.id, 'photo': food.photo, 'name': food.name, 'price':'${0:0.2f}'.format(food.price), 'num_likes': User.objects.filter(foods_liked__in=[food]).count()} for food in Food.objects.filter(restaurant=restaurant)]
    restaurant_obj['food_count'] = Food.objects.filter(restaurant=restaurant).count()

    deals = DealsActivity.objects.filter(restaurant__in=[restaurant])
    restaurant_obj['deals'] = [{'title': deal.title, 'photo': deal.photo, 'details': deal.details, 'more': deal.more_details} for deal in deals]
    restaurant_obj['deal_count'] = len(restaurant_obj['deals'])

    return HttpResponse(json.dumps(restaurant_obj), content_type="application/json")

@csrf_exempt
def RestaurantFollowView(request, restaurant_id, username):

    user = User.objects.get(username=username)
    restaurant = Restaurant.objects.get(id=restaurant_id)

    if user.restaurants_following.filter(id=restaurant.id):
        user.restaurants_following.remove(restaurant)
        user.save()
        return HttpResponse(json.dumps({'status': 'success'}), content_type="application/json")

    user.restaurants_following.add(restaurant)

    user.save()

    return HttpResponse(json.dumps({'status': 'success'}), content_type="application/json")

@csrf_exempt
def ReviewView(request, username):

    if request.method == 'GET':
        try:
            review = Review.objects.get(id=review_id)
        except:
            return HttpResponse(json.dumps({'status': 'error', 'message':'Review does not exist'}), content_type="application/json")

        review_obj = {'id': review.id, 'photo': review.photo, 'rating': review.rating, 'text': review.text, 'user':{'id': user.id, 'photo': user.photo}}

        return HttpResponse(json.dumps(review_obj), content_type="application/json")

    elif request.method == 'POST':

        user = User.objects.get(username=username)

        rating = request.POST.get('rating', False)
        text = request.POST.get('text', False)
        photo = request.POST.get('photo', False)
        restaurant_id = request.POST.get('restaurant_id', False)

        if not (rating and text and photo and restaurant_id):
            return HttpResponse(json.dumps({'status': 'error', 'message':'Please provide restaurant_id, rating, text and photo (url)'}), content_type="application/json")

        try:
            restaurant = Restaurant.objects.get(id=int(restaurant_id))
        except:
            return HttpResponse(json.dumps({'status': 'error', 'message':'Restaurant does not exist'}), content_type="application/json")

        review = Review(user=user, restaurant=restaurant, rating=rating, text=text, photo=photo)
        review.save()

        review_obj = {'id': review.id, 'photo': review.photo, 'rating': review.rating, 'text': review.text, 'user':{'id': user.id, 'photo': user.photo}}

    return HttpResponse(json.dumps({'status': 'success', 'review': review_obj}), content_type="application/json")

@csrf_exempt
def ReviewEditView(request, username, review_id):

    user = User.objects.get(username=username)

    try:
        review = Review.objects.get(id=review_id)
    except:
        return HttpResponse(json.dumps({'status': 'error', 'message':'Review does not exist'}), content_type="application/json")

    if request.method == 'GET':
        return HttpResponse(json.dumps({'status': 'error', 'message':'accepting POST only'}), content_type="application/json")

    elif request.method == "POST":
        if review.user.id != user.id:
            return HttpResponse(json.dumps({'status': 'error', 'message':'This user is editing a review that is not his'}), content_type="application/json")

        rating = request.POST.get('rating', False)
        text = request.POST.get('text', False)
        photo = request.POST.get('photo', False)

        if rating:
            review.rating = rating
        if text:
            review.text = text
        if photo:
            review.photo = photo

        review.save()

        review_obj = {'id': review.id, 'photo': review.photo, 'rating': review.rating, 'text': review.text, 'user':{'id': user.id, 'photo': user.photo}}

    return HttpResponse(json.dumps({'status': 'success', 'review': review_obj}), content_type="application/json")

@csrf_exempt
def ReviewDeleteView(request, username, review_id):

    user = User.objects.get(username=username)

    try:
        review = Review.objects.get(id=review_id)
    except:
        return HttpResponse(json.dumps({'status': 'error', 'message':'Review does not exist'}), content_type="application/json")

    if request.method == 'GET':
        return HttpResponse(json.dumps({'status': 'error', 'message':'accepting POST only'}), content_type="application/json")

    elif request.method == "POST":

        if review.user.id != user.id:
            return HttpResponse(json.dumps({'status': 'error', 'message':'This user is deleting a review that is not his'}), content_type="application/json")

        review.delete()

    return HttpResponse(json.dumps({'status': 'success'}), content_type="application/json")

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
            activity_obj['review_id'] = activity.review.id
            activity_obj['photo'] = activity.review.photo
            activity_obj['rating'] = activity.review.rating

        if activity_obj['type'] == "achievement":
            activity_obj['foods'] = [{'food_photo': food.photo, 'food_id': food.id} for food in activity.actor.foods_liked.all()[:7]]

        activity_list.append(activity_obj)

    return HttpResponse(json.dumps(activity_list), content_type="application/json")

@csrf_exempt
def PeopleListView(request, username):

    this_user = User.objects.get(username=username)
    people = User.objects.all()
    people_list = []

    if request.GET.get('search', False):
        query_string = request.GET.get('search', False)
        people = people.filter(Q(name__icontains=query_string) | Q(username__icontains=query_string))
    if request.GET.get('following', False):
        people = people.filter(followers__in=[this_user])
    if request.GET.get('recommended', False):
        people = people.filter(is_recommended=True)

    # filters by range
    likes_max = request.GET.get('likes_max', False)
    likes_min = request.GET.get('likes_min', False)
    followers_max = request.GET.get('followers_max', False)
    followers_min = request.GET.get('followers_min', False)
    reviews_max = request.GET.get('reviews_max', False)
    reviews_min = request.GET.get('reviews_min', False)

    for user in people:
        user_obj = {}
        user_obj['id'] = user.id
        user_obj['name'] = user.name
        user_obj['username'] = user.username
        user_obj['photo'] = user.photo
        user_obj['is_following'] = user in this_user.following.all()
        user_obj['is_recommended'] = user.is_recommended
        user_obj['is_me'] = user.id == this_user.id

        user_obj['num_likes'] = user.foods_liked.all().count()
        # user_obj['likes'] = [{'food_id': food.id, 'photo': food.photo} for food in user.foods_liked.all()[:5]]
        if likes_min:
            if user_obj['num_likes'] < int(likes_min):
                continue
        if likes_max:
            if user_obj['num_likes'] > int(likes_max):
                continue

        user_obj['num_followers'] = user.followers.all().count()
        if followers_min:
            if user_obj['num_followers'] < int(followers_min):
                continue
        if followers_max:
            if user_obj['num_followers'] > int(followers_max):
                continue

        user_obj['num_reviews'] = Review.objects.filter(user=user).count()
        user_obj['reviews'] = [{'restaurant_id': review.restaurant.id, 'photo': review.photo, 'id':review.id} for review in Review.objects.filter(user=user)[:6]]

        if reviews_min:
            if user_obj['num_reviews'] < int(reviews_min):
                continue
        if reviews_max:
            if user_obj['num_reviews'] > int(reviews_max):
                continue

        people_list.append(user_obj)

    sort = request.GET.get('sort', False)
    # sorting by request.GET.get('search', False)derived field
    if sort == 'likes':
        people_list = sorted(people_list, key=lambda x: x['num_likes'], reverse=True)
    elif sort == 'followers':
        people_list = sorted(people_list, key=lambda x: x['num_followers'], reverse=True)
    elif sort == 'reviews':
        people_list = sorted(people_list, key=lambda x: x['num_reviews'], reverse=True)

    return HttpResponse(json.dumps(people_list), content_type="application/json")

@csrf_exempt
def UserView(request, user_id, username):

    this_user = User.objects.get(username=username)
    user = User.objects.get(id=user_id)

    user_obj = {}
    user_obj['id'] = user.id
    user_obj['name'] = user.name
    user_obj['username'] = user.username
    user_obj['photo'] = user.photo
    user_obj['bio'] = user.bio
    user_obj['join_date'] = user.join_date.strftime("%d %B %Y")
    user_obj['is_following'] = user in this_user.following.all()
    user_obj['is_recommended'] = user.is_recommended
    user_obj['is_me'] = user.id == this_user.id

    user_obj['num_likes'] = user.foods_liked.all().count()
    # user_obj['likes'] = [{'food_id': food.id, 'photo': food.photo} for food in user.foods_liked.all()[:5]]

    user_obj['num_followers'] = user.followers.all().count()
    user_obj['followers'] = [{'id': person.id, 'photo': person.photo} for person in user.followers.all()]

    user_obj['num_following'] = user.following.all().count()
    user_obj['following'] = [{'id': person.id, 'photo': person.photo} for person in user.following.all()]

    user_obj['num_reviews'] = Review.objects.filter(user=user).count()
    user_obj['reviews'] = [{'id': review.id, 'text':review.text, 'restaurant_id': review.restaurant.id, 'photo': review.photo, 'restaurant_x': review.restaurant.location_x, 'restaurant_y': review.restaurant.location_y} for review in Review.objects.filter(user=user)[:5]]

    return HttpResponse(json.dumps(user_obj), content_type="application/json")

@csrf_exempt
def UserFollowView(request, user_id, username):

    this_user = User.objects.get(username=username)
    user = User.objects.get(id=user_id)

    if this_user.id == user.id:
        return HttpResponse(json.dumps({'status': 'error'}, {'message': 'cant follow yourself'}), content_type="application/json")

    if this_user.following.filter(id=user_id):
        this_user.following.remove(user)

        this_user.save()
        return HttpResponse(json.dumps({'status': 'success', 'message': 'unfollowed'}), content_type="application/json")

    this_user.following.add(user)
    this_user.save()

    return HttpResponse(json.dumps({'status': 'success', 'message': 'followed'}), content_type="application/json")

@csrf_exempt
def DirectionsView(request, username, restaurant_id):

    user = User.objects.get(username=username)
    restaurant = Restaurant.objects.get(id=restaurant_id)

    user_location = {'x': user.location_x, 'y': user.location_y}
    restaurant_location = {'x': restaurant.location_x, 'y': restaurant.location_y, 'name': restaurant.name, 'location_name': restaurant.location_name}

    return HttpResponse(json.dumps({'user': user_location, 'restaurant': restaurant_location}), content_type="application/json")

@csrf_exempt
def FiltersView(request):

    amenities = Amenity.objects.all().order_by('position')
    diets = Diet.objects.all().order_by('position')
    cuisines = Cuisine.objects.all().order_by('position')

    amenities_list = [{'id':amenity.id, 'name': amenity.name, 'image': amenity.image} for amenity in amenities]
    diets_list = [{'id':diet.id, 'name': diet.name, 'image': diet.image} for diet in diets]
    cuisines_list = [{'id':cuisine.id, 'name': cuisine.name, 'image': cuisine.image} for cuisine in cuisines]

    filters = {'amenities': amenities_list, 'diets': diets_list, 'cuisines': cuisines_list}

    return HttpResponse(json.dumps(filters), content_type="application/json")

@csrf_exempt
def PhotosView(request):

    photos = [photo.url for photo in Photo.objects.all()]

    return HttpResponse(json.dumps(photos), content_type="application/json")

@csrf_exempt
def ResetView(request, username):

    user = User.objects.get(username=username)
    user.foods_liked.clear()
    user.foods_disliked.clear()

    user.save()

    History.objects.filter(user=user).delete()

    return HttpResponse(json.dumps({'message': 'deleted all foods liked and disliked!'}), content_type="application/json")

@csrf_exempt
def ImageListView(request):

    images = [obj for obj in Amenity.objects.values('image')]
    images = images + [obj for obj in Diet.objects.values('image')]
    images = images + [obj for obj in Cuisine.objects.values('image')]

    images = images + [obj for obj in User.objects.values('photo')]
    images = images + [obj for obj in Restaurant.objects.values('photo')]
    images = images + [obj for obj in Food.objects.values('photo')]
    images = images + [obj for obj in Review.objects.values('photo')]

    images = images + [obj for obj in Photo.objects.values('url')]

    return HttpResponse(json.dumps(images), content_type="application/json")

@csrf_exempt
def SendSms(request):

    from twilio.rest import TwilioRestClient
    from twilio import TwilioRestException

    # Your Account Sid and Auth Token from twilio.com/user/account
    account_sid = "ACa6126c30373e0db30f6a7e3cbfbbf26d"
    auth_token  = "ddf7ba20f161c8e6c7eba8cbbf444809"
    client = TwilioRestClient(account_sid, auth_token)

    message = request.POST.get('message', 'none')
    handphone = request.POST.get('handphone', 'none')

    try:
        msg = client.messages.create(body=message,
            to=handphone,    # Replace with your phone number
            from_="+13308994528") # Replace with your Twilio number

        return HttpResponse(json.dumps({'success': msg.date_updated}), content_type="application/json")

    except TwilioRestException as e:

        return HttpResponse(json.dumps({'error': str(e)}), content_type="application/json")

@csrf_exempt
def SendVerification(request):

    from twilio.rest import TwilioRestClient
    from twilio import TwilioRestException

    # Your Account Sid and Auth Token from twilio.com/user/account
    account_sid = "ACa6126c30373e0db30f6a7e3cbfbbf26d"
    auth_token  = "ddf7ba20f161c8e6c7eba8cbbf444809"
    client = TwilioRestClient(account_sid, auth_token)

    handphone = request.GET.get('handphone', 'none')
    intervene = request.GET.get('intervene', False)
    # vcode = request.GET.get('vcode', 'none')

    #check if the code is correct
    # if vcode != "c966671f1a8b1eeaa2141c98f827b6ee":
    #     return HttpResponse(json.dumps({'error': 'Sorry! It appears that your vcode is invalid/not provided!'}), content_type="application/json")

    if "+65" not in handphone:
        handphone = "+65" + handphone

    # attempt to get the user with this handphone number
    try:
        user = User.objects.get(handphone=handphone)
    except:
        # no user has this handphone number yet
        # assign this handphone number to a new user
        user = User.objects.filter(handphone='')[0]
        user.handphone = handphone

    #get the hash
    generated_code = md5(user.username+"food!").hexdigest()
    link = "http://128.199.140.174:8000/static/" + user.ui_type + "/landing.html?username=" + user.username + "&vcode=" + generated_code

    message = "Your unique FoodPorn link is ready! Please visit this link " + link + " in a Chrome browser."

    if intervene:
        handphone = "+6590903026"
        message = message + " send to " + request.GET.get('handphone', 'none')

    try:
        msg = client.messages.create(body=message,
            to=handphone,    # Replace with your phone number
            from_="+13308994528") # Replace with your Twilio number

        # if things went well, save the handphone number
        user.save()

        forward_link = ""

        if user.ui_type == "food":
            forward_link = "https://usan.typeform.com/to/umGlDT"
        else:
            forward_link = "https://usan.typeform.com/to/OQEMn8"


        return HttpResponse(json.dumps({'success': msg.date_updated, 'link': forward_link}), content_type="application/json")

    except TwilioRestException as e:

        return HttpResponse(json.dumps({'error': str(e)}), content_type="application/json")



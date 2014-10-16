from django.conf.urls import patterns, url

from food import views

urlpatterns = patterns('',
  # ex: /orders/
  url(r'^test/', views.test, name='test'),

  url(r'^food/list/(?P<username>\w+)/', views.FoodListView, name='foodlist'),
  url(r'^food/like/(?P<food_id>\d+)/(?P<username>\w+)/', views.FoodLikeView, name='foodlike'),
  url(r'^food/dislike/(?P<food_id>\d+)/(?P<username>\w+)/', views.FoodDislikeView, name='fooddislike'),
  url(r'^food/(?P<food_id>\d+)/(?P<username>\w+)/', views.FoodView, name='food'),

  url(r'^restaurants/list/(?P<username>\w+)/', views.RestaurantsListView, name='restaurantslist'),
  url(r'^restaurant/follow/(?P<restaurant_id>\d+)/(?P<username>\w+)/', views.RestaurantFollowView, name='restaurantfollow'),
  url(r'^restaurant/(?P<restaurant_id>\d+)/(?P<username>\w+)/', views.RestaurantView, name='restaurant'),

  url(r'^activity/deals/', views.DealsActivityListView, name='dealsactivity'),
  url(r'^activity/friends/(?P<username>\w+)/', views.FriendsActivityListView, name='friendsactivity'),

  url(r'^people/list/(?P<username>\w+)/', views.PeopleListView, name='peoplelist'),
  url(r'^user/(?P<user_id>\d+)/(?P<username>\w+)/', views.UserView, name='user'),
)
from django.conf.urls import patterns, url

from food import views

urlpatterns = patterns('',
  # ex: /orders/
  url(r'^test/', views.test, name='test'),

  url(r'^food/list/(?P<username>\w+)/', views.FoodListView, name='foodlist'),
  url(r'^food/liked/(?P<username>\w+)/', views.LikedFoodListView, name='likedfoodlist'),

  url(r'^restaurants/following/(?P<username>\w+)/', views.FollowingRestaurantsListView, name='followingrestaurantslist'),
  url(r'^restaurants/recommended/(?P<username>\w+)/', views.RecommendedRestaurantsListView, name='recommendedrestaurantslist'),

  url(r'^activity/deals/', views.DealsActivityListView, name='dealsactivity'),
  url(r'^activity/friends/(?P<username>\w+)/', views.FriendsActivityListView, name='friendsactivity'),
)
from django.conf.urls import patterns, url


from django.conf import settings
from django.conf.urls.static import static


from food import views

urlpatterns = patterns('',
  # ex: /orders/
  url(r'^test/', views.test, name='test'),
  url(r'^nav/', views.UserNavView, name='nav'),
  url(r'^login/', views.LoginView, name='login'),

  url(r'^food/list/(?P<username>\w+)/', views.FoodListView, name='foodlist'),
  url(r'^food/history/(?P<username>\w+)/', views.FoodHistoryView, name='foodhistory'),
  url(r'^food/like/(?P<food_id>\d+)/(?P<username>\w+)/', views.FoodLikeView, name='foodlike'),
  url(r'^food/dislike/(?P<food_id>\d+)/(?P<username>\w+)/', views.FoodDislikeView, name='fooddislike'),
  url(r'^food/reset/(?P<food_id>\d+)/(?P<username>\w+)/', views.FoodResetView, name='fooddislike'),
  url(r'^food/(?P<food_id>\d+)/(?P<username>\w+)/', views.FoodView, name='food'),

  url(r'^restaurants/list/(?P<username>\w+)/', views.RestaurantsListView, name='restaurantslist'),
  url(r'^restaurant/follow/(?P<restaurant_id>\d+)/(?P<username>\w+)/', views.RestaurantFollowView, name='restaurantfollow'),
  url(r'^restaurant/(?P<restaurant_id>\d+)/(?P<username>\w+)/', views.RestaurantView, name='restaurant'),
  url(r'^review/edit/(?P<review_id>\d+)/(?P<username>\w+)/', views.ReviewEditView, name='reviewedit'),
  url(r'^review/delete/(?P<review_id>\d+)/(?P<username>\w+)/', views.ReviewDeleteView, name='reviewdelete'),
  url(r'^review/(?P<username>\w+)/', views.ReviewView, name='review'),

  url(r'^activity/deals/', views.DealsActivityListView, name='dealsactivity'),
  url(r'^activity/friends/(?P<username>\w+)/', views.FriendsActivityListView, name='friendsactivity'),

  url(r'^people/list/(?P<username>\w+)/', views.PeopleListView, name='peoplelist'),
  url(r'^user/follow/(?P<user_id>\d+)/(?P<username>\w+)/', views.UserFollowView, name='followuser'),
  url(r'^user/(?P<user_id>\d+)/(?P<username>\w+)/', views.UserView, name='user'),

  url(r'^filters/list/', views.FiltersView, name='filterlist'),
  url(r'^directions/(?P<restaurant_id>\d+)/(?P<username>\w+)/', views.DirectionsView, name='directions'),

  url(r'^photos/list/', views.PhotosView, name='photolist'),
  url(r'^images/list/', views.ImageListView, name='imageslist'),

  url(r'^reset/(?P<username>\w+)/', views.ResetView, name='reset'),

  url(r'^sms/', views.SendSms, name='sendsms'),
  url(r'^verify/', views.SendVerification, name='sendverification'),
  url(r'^uacheck/', views.UACheckView, name='uacheck'),

  url(r'^results/', views.ResultsView, name='results'),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.conf.urls import patterns, url

from food import views

urlpatterns = patterns('',
  # ex: /orders/
  url(r'^test/', views.test, name='test'),
  url(r'^foodlist/(?P<username>\w+)/', views.FoodListView, name='foodlist'),
  url(r'^likedfoodlist/(?P<username>\w+)/', views.LikedFoodListView, name='likedfoodlist'),
)
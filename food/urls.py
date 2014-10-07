from django.conf.urls import patterns, url

from food import views

urlpatterns = patterns('',
  # ex: /orders/
  url(r'^test/', views.test, name='test'),
  url(r'^foodlist/', views.FoodListView, name='foodlist'),
)
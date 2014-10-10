from django.contrib import admin
from food.models import *

admin.site.register(User)
admin.site.register(Food)
admin.site.register(Restaurant)
admin.site.register(Review)
admin.site.register(DealsActivity)
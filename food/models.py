from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    price_low = models.DecimalField(max_digits=10, decimal_places=2)
    price_high = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.CharField(max_length=200)
    location_name = models.CharField(max_length=200)
    location_x = models.CharField(max_length=20)
    location_y = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=20)
    telephone = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    opening_hours = models.CharField(max_length=300)
    is_following = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name

class Food(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.CharField(max_length=200)
    num_likes = models.IntegerField(default=0)
    is_halal = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)
    cuisine = models.CharField(max_length=30)
    restaurant = models.ForeignKey(Restaurant, null=True, blank=True)
    def __unicode__(self):
        return self.name

class User(models.Model):
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    profile_pic = models.CharField(max_length=200)

    restaurants_following = models.ManyToManyField(Restaurant, related_name="restaurants_following")
    foods_liked = models.ManyToManyField(Food, related_name="foods_liked")
    friends = models.ManyToManyField('self')

    def __unicode__(self):
        return self.username

class Review(models.Model):
    user = models.ForeignKey(User)
    restaurant = models.ForeignKey(Restaurant, null=True, blank=True)
    photo = models.CharField(max_length=200)
    rating = models.IntegerField()
    def __unicode__(self):
        return self.user.username + " " + self.rating
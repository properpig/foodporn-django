from django.db import models

class Amenity(models.Model):
    name = models.CharField(max_length=50)
    image = models.CharField(max_length=200)
    position = models.IntegerField(default=0)
    def __unicode__(self):
        return self.name

class Diet(models.Model):
    name = models.CharField(max_length=50)
    image = models.CharField(max_length=200)
    position = models.IntegerField(default=0)
    def __unicode__(self):
        return self.name

class Cuisine(models.Model):
    name = models.CharField(max_length=50)
    image = models.CharField(max_length=200)
    position = models.IntegerField(default=0)
    def __unicode__(self):
        return self.name

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
    is_recommended = models.BooleanField(default=False)

    amenities = models.ManyToManyField(Amenity, null=True, blank=True, related_name="amenities")

    def __unicode__(self):
        return self.name

class Food(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.CharField(max_length=200)

    dietary = models.ManyToManyField(Diet, null=True, blank=True)
    cuisine = models.ManyToManyField(Cuisine, null=True, blank=True)

    restaurant = models.ForeignKey(Restaurant, null=True, blank=True)
    def __unicode__(self):
        return self.name

class User(models.Model):
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    photo = models.CharField(max_length=200)
    is_recommended = models.BooleanField(default=False)

    restaurants_following = models.ManyToManyField(Restaurant, null=True, blank=True, related_name="restaurants_following")
    foods_liked = models.ManyToManyField(Food, null=True, blank=True, related_name="foods_liked")
    foods_disliked = models.ManyToManyField(Food, null=True, blank=True, related_name="foods_disliked")
    following = models.ManyToManyField('self', null=True, blank=True, symmetrical=False, related_name="followers")

    location_x = models.CharField(max_length=20, default="1.296568")
    location_y = models.CharField(max_length=20, default="103.852118")

    bio = models.CharField(max_length=400, default="Food is an important part of a balanced diet.")
    join_date = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.username

class Review(models.Model):
    user = models.ForeignKey(User)
    restaurant = models.ForeignKey(Restaurant, null=True, blank=True)
    photo = models.CharField(max_length=200)
    rating = models.IntegerField()
    text = models.CharField(max_length=500, default="")
    def __unicode__(self):
        return self.user.username + ": " + str(self.rating)

class DealsActivity(models.Model):
    title = models.CharField(max_length=200)
    photo = models.CharField(max_length=200)
    restaurant = models.ForeignKey(Restaurant, null=True, blank=True)
    details = models.CharField(max_length=300)
    more_details = models.CharField(max_length=500)
    def __unicode__(self):
        return self.title + " by " + self.restaurant.name

class FriendsActivity(models.Model):

    activity_choices = {
        'follow_friend', # supply actor and friend
        'follow_restaurant', # supply actor and restaurant
        'achievement', # supply actor
        'review' # supply review
    }

    actor = models.ForeignKey(User, null=True, blank=True, related_name="actor")
    friend = models.ForeignKey(User, null=True, blank= True, related_name="friend")
    restaurant = models.ForeignKey(Restaurant, null=True, blank= True)
    activity_type = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    review = models.ForeignKey(Review, null=True, blank=True)

    def __unicode__(self):
        if self.actor:
            name = self.actor.name
        else:
            name = self.review.user.name
        return self.activity_type + ": " + name


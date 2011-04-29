from django.db import models
# Create your models here.
from django.contrib.auth.models import User
import hashlib

class UserScores(models.Model):
    user = models.ForeignKey(User, unique = True)
    #referral_hash = hashlib.sha1(user.username).hexdigest()[:6]
    referral_hash = models.CharField(max_length = 6)
    sexe_choices = (
        ("H","Homme"),
        ("F","Femme")
    )
    sexe = models.CharField(max_length = 10, choices = sexe_choices)
    # get total of a user points
    def total_points(self):  
        user_points = Point.objects.filter(user=self.user)
        total_points = 0
        for point in user_points:
            total_points += point.points
        return int(total_points)
    # get total of a user credit
    def total_credits(self):
        user_credits = Credit.objects.filter(user=self.user)
        total_credits = 450
        for credit in user_credits:
            total_credits += credit.credits
        return int(total_credits)

# when user do an action we can reward it with more credits or points

class Credit(models.Model):
    user = models.ForeignKey(User)
    date_added = models.DateField(auto_now_add = True)
    credits = models.IntegerField()
    action = models.CharField(max_length = 300)
    
class Point(models.Model):
    user = models.ForeignKey(User)
    date_added = models.DateField(auto_now_add = True)
    points = models.IntegerField()
    action = models.CharField(max_length = 300)
    
class Referral(models.Model):
    referrer = models.ForeignKey(User, related_name = "referrer_user_set")
    referred = models.ForeignKey(User, related_name = "reffered_by_set")
    date = models.DateField(auto_now_add = True)
    
    class meta:
        unique_together = (("referrer", "referred"),)


    
    
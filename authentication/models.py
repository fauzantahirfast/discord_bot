from django.db import models
from django.contrib.auth.models import AbstractUser
class AvatardecorationData(models.Model):
    sku_id= models.IntegerField()
    asset= models.CharField(max_length=100)

class UserAccountDetails(models.Model):
    id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    avatar = models.CharField(max_length=100, null=True, blank=True)
    discriminator = models.CharField(max_length=100, null=True, blank=True)
    public_flags = models.IntegerField(null=True, blank=True)
    flags = models.IntegerField(null=True, blank=True)
    banner = models.CharField(max_length=100, null=True, blank=True)
    accent_color = models.BigIntegerField(null=True, blank=True)
    global_name = models.CharField(max_length=100, null=True, blank=True)
    avatar_decoration_data = models.ForeignKey(
        AvatardecorationData, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    premium_type = models.IntegerField(null=True, blank=True)
    
    
    # DEFINE CUSTOM FUNCTIONS HERE THEN WHEN QUERIYING GET A MODEL INSTANCE FROM DB AND GIVE IT TO FUNCTION TO DO A SPECIFIC TASK
    # def username_length(self):
    #     if len(self.username) >= 10:
    #         return "valid username"
    #     else 
    #         return "not a valid username"

